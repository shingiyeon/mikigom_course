#!/usr/bin/python3
import sys
import subprocess
import os
import inspect

esp = 0
ebp = 0
vname = ""

def TBI():
    print("WRANING: TBI in %s at %s:%d" % (
            inspect.currentframe().f_back.f_code.co_name,
            inspect.currentframe().f_back.f_code.co_filename,
            inspect.currentframe().f_back.f_lineno))

# Nodes types.
CAST_TRANSLATION_UNIT,\
CAST_FUN_DEFINITION,\
CAST_PAR_TYPE_LIST,\
CAST_PAR_TYPE,\
CAST_VAR_DECLARATION,\
CAST_IF_STMT,\
CAST_WHILE_STMT,\
CAST_RETURN_STMT,\
CAST_COMP_STMT,\
CAST_DECL_LIST, \
CAST_STMT_LIST, \
CAST_EXPR_STMT,\
CAST_EQ_EXPR, \
CAST_NOT_EQ_EXPR, \
CAST_LESS_EXPR, \
CAST_GREATER_EXPR,\
CAST_LESS_EQ_EXPR,\
CAST_GREATER_EQ_EXPR,\
CAST_PLUS_EXPR,\
CAST_MINUS_EXPR,\
CAST_MUL_EXPR,\
CAST_DIV_EXPR,\
CAST_MOD_EXPR,\
CAST_VAR_EXPR,\
CAST_CALL_EXPR,\
CAST_INT_CONST_EXPR,\
CAST_ARG_LIST,\
= range(27)

# String representations of node types.
CAST_NODE_STR={
  CAST_TRANSLATION_UNIT: "CAST_TRANSLATION_UNIT",
  CAST_FUN_DEFINITION: "CAST_FUN_DEFINITION",
  CAST_PAR_TYPE_LIST: "CAST_PAR_TYPE_LIST",
  CAST_PAR_TYPE: "CAST_PAR_TYPE",
  CAST_VAR_DECLARATION: "CAST_VAR_DECLARATION",
  CAST_IF_STMT: "CAST_IF_STMT",
  CAST_WHILE_STMT: "CAST_WHILE_STMT",
  CAST_RETURN_STMT: "CAST_RETURN_STMT",
  CAST_COMP_STMT: "CAST_COMP_STMT",
  CAST_DECL_LIST : "CAST_DECL_LIST",
  CAST_STMT_LIST : "CAST_STMT_LIST",
  CAST_EXPR_STMT: "CAST_EXPR_STMT",
  CAST_EQ_EXPR : "CAST_EQ_EXPR",
  CAST_NOT_EQ_EXPR : "CAST_NOT_EQ_EXPR",
  CAST_LESS_EXPR : "CAST_LESS_EXPR",
  CAST_GREATER_EXPR: "CAST_GREATER_EXPR",
  CAST_LESS_EQ_EXPR: "CAST_LESS_EQ_EXPR",
  CAST_GREATER_EQ_EXPR: "CAST_GREATER_EQ_EXPR",
  CAST_PLUS_EXPR: "CAST_PLUS_EXPR",
  CAST_MINUS_EXPR: "CAST_MINUS_EXPR",
  CAST_MUL_EXPR: "CAST_MUL_EXPR",
  CAST_DIV_EXPR: "CAST_DIV_EXPR",
  CAST_MOD_EXPR: "CAST_MOD_EXPR",
  CAST_VAR_EXPR: "CAST_VAR_EXPR",
  CAST_CALL_EXPR: "CAST_CALL_EXPR",
  CAST_INT_CONST_EXPR: "CAST_INT_CONST_EXPR",
  CAST_ARG_LIST: "CAST_ARG_LIST",
}

def cast_get_node_type(n):
    return n[0]

def cast_set_attribute(n, aname, value):
    n[1][aname]=value

def cast_get_attribute(n, aname):
    return n[1][aname]

def cast_get_child(n, i):
    return n[2+i]

def cast_get_children(n):
    return n[2:]

# Dump an abstract syntax tree into its list representation in Python.
def cast_dump(r):
    s={'depth':-1}
    def depth(): 
        return s['depth']
    def enter(): 
        s['depth'] += 1
    def leave(): 
        s['depth'] -= 1
    def tab():
        s = ""
        for i in range(depth()): 
            s = s + "  "
        return s
    def visit(n):
        enter()
        t=n[0]
        tname=CAST_NODE_STR[t]
        attrs=[]
        for aname in n[1]:
            value=n[1][aname]
            if isinstance(value, str):
                val_str='"%s"' % value
            elif isinstance(value, int):
                val_str='%d' % value
            elif isinstance(value, list):
                val_str='%s' % value
            else:
                assert False
            attrs.append("'%s': %s" % (aname, val_str))
        attrs=', '.join(attrs)
        children=n[2:]
        print("%s[%s, {%s}" % (tab(), tname, attrs),end='' if len(children) == 0 else ',\n')
        for c in n[2:]:
            visit(c)
        if len(children) == 0:
            print("],")
        else:
            if n == r:
                print("%s]" % (tab()))
            else:
                print("%s]," % (tab()))
        leave()
    print("AST= \\")
    visit(r)


# semantic analysis of binding identifiers to their binding information of the following form
#   * binding for functions: [BINDING_FUNCTION %name% %storage size for local variables%]
#   * binding fof variables: [BINDING_VARIABLE %offset from the frame pointer%
BINDING_FUNCTION, \
BINDING_VARIABLE, \
=range(2)

def cast_analyze(r):
    stab=[{}]
    def stab_lookup(sym):
        for tab in reversed(stab):
            if sym in tab:
                return tab[sym]
        return None
    def stab_put(sym, binding):
        assert binding != None
        stab[-1][sym]=binding
    def stab_enterScope():
        stab.append({})
    def stab_leaveScope():
        stab.pop()
    def visit(n,args=None):
        global esp, ebp, vname
        ntype=cast_get_node_type(n)
        if ntype == CAST_TRANSLATION_UNIT:
            for c in cast_get_children(n):
                visit(c)            
        elif ntype == CAST_FUN_DEFINITION:
            esp = 4
            ebp = 0
            fname=cast_get_attribute(n, 'id')
            binding=[BINDING_FUNCTION, fname, 0]
            stab_put(fname, binding)
            stab_put("__current_function__", binding)
            cast_set_attribute(n, 'binding', binding)
            stab_enterScope()
            params = cast_get_children(cast_get_child(n, 0))
            for c in cast_get_children(n):
                visit(c)
            for tab in reversed(stab):
                if fname in tab:
                    tab[fname][2] = -ebp
                    ebp = 0
            stab_leaveScope()
        elif ntype in [CAST_PAR_TYPE_LIST, CAST_STMT_LIST, CAST_COMP_STMT, CAST_DECL_LIST, CAST_WHILE_STMT, CAST_DECL_LIST, CAST_COMP_STMT, CAST_DECL_LIST, CAST_WHILE_STMT, CAST_NOT_EQ_EXPR, CAST_IF_STMT, CAST_NOT_EQ_EXPR, CAST_IF_STMT, CAST_GREATER_EXPR, CAST_EXPR_STMT, CAST_MINUS_EXPR, CAST_RETURN_STMT, CAST_EQ_EXPR, CAST_INT_CONST_EXPR]:
            for c in cast_get_children(n):
                visit(c)
        elif ntype == CAST_PAR_TYPE:
            esp = esp + 4
            vname=cast_get_attribute(n, 'id')
            binding=[BINDING_VARIABLE, esp]
            stab_put(vname, binding)
            cast_set_attribute(n, 'binding', binding)
            for c in cast_get_children(n):
                visit(c)
        elif ntype == CAST_VAR_DECLARATION:
            ebp = ebp - 4
            vname=cast_get_attribute(n, 'id')
            binding=[BINDING_VARIABLE, ebp]
            stab_put(vname, binding)
            cast_set_attribute(n, 'binding', binding)
            for c in cast_get_children(n):
                visit(c)
        elif ntype == CAST_VAR_EXPR:
            vname = cast_get_attribute(n, 'id')
            binding=stab_lookup(vname)
            cast_set_attribute(n, 'binding', binding)
            for c in cast_get_children(n):
                visit(c)
        elif ntype == CAST_CALL_EXPR:
            fname = cast_get_attribute(n, 'fname')
            binding = stab_lookup(fname)
            cast_set_attribute(n, 'binding', binding)
            for c in cast_get_children(n):
                visit(c)
    visit(r)


# Intermediate representations
PROLOGUE, \
MOV, \
PUSH, \
POP, \
ADD, \
SUB, \
JMP, \
CMP, \
JE, \
JNE, \
JG, \
JGE, \
JL, \
JLE, \
CALL,\
RET, \
LABEL, \
LEAVE, \
= range(18)


OPCODE2STR={
  PROLOGUE: "PROLOGUE",
  MOV: "MOV",
  PUSH: "PUSH",
  POP: "POP",
  ADD: "ADD",
  SUB: "SUB",
  JMP: "JMP",
  CMP: "CMP",
  JE: "JE",
  JNE: "JNE",
  JG: "JG",
  JGE: "JGE",
  JL: "JL",
  JLE: "JLE",
  CALL: "CALL",
  RET: "RET",
  LABEL: "LABEL",
  LEAVE: "LEAVE",
}

REG, \
IMM, \
MEM, \
= range(3)

OPERAND2STR={
  REG: "REG",
  IMM: "IMM",
  MEM: "MEM",
}

EAX = 0
ECX = 1
EDX = 2
EBX = 3
ESP = 4
EBP = 5
ESI = 6
EDI = 7

PHY_REG2STR = {
    EAX: "EAX",
    ECX: "ECX",
    EDX: "EDX",
    EBX: "EBX",
    ESP: "ESP",
    EBP: "EBP",
    ESI: "ESI",
    EDI: "EDI",
}

NAMES = {
    EAX: "%eax",
    ECX: "%ecx",
    EDX: "%edx",
    EBX: "%ebx",
    ESP: "%esp",
    EBP: "%ebp",
    ESI: "%esi",
    EDI: "%edi",
}

VOLATILE_REGISTERS=set([
        EAX,
        ECX,
        EDX,
])

NONVOLATILE_REGISTERS=set([
        EBX,
        EDI,
        ESI,
])

VIRTUAL_REG_BEGIN=8

def MOV_Reg_Reg(dstReg, srcReg):
    return (MOV, (REG, dstReg), (REG, srcReg))

def MOV_RegDisp_Reg(dstBase, dstDisp, srcReg):
    return (MOV, (MEM, (REG, dstBase), dstDisp), (REG, srcReg))

def MOV_Reg_RegDisp(dstReg, srcBase, srcDisp):
    return (MOV, (REG, dstReg), (MEM, (REG, srcBase), srcDisp))

def MOV_Reg_Imm(dstReg, imm):
    return (MOV, (REG, dstReg), (IMM, imm))

def PUSH_Reg(reg):
    return (PUSH, (REG, reg))

def POP_Reg(reg):
    return (POP, (REG, reg))

def ADD_Reg_Reg(dstReg, srcReg):
    return (ADD, (REG, dstReg), (REG, srcReg))

def ADD_Reg_Imm(dstReg, imm):
    return (ADD, (REG, dstReg), (IMM, imm))

def SUB_Reg_Reg(dstReg,srcReg):
    return (SUB, (REG, dstReg), (REG, srcReg))

def SUB_RegDisp_Reg(dstReg, dstDisp, srcReg):
    return (SUB, (MEM, (REG, dstReg), dstDisp), (REG, srcReg))

def CMP_Reg_imm(reg, imm):
    return (CMP, (REG, reg), (IMM, imm))

def CMP_Reg_Reg(dstReg, srcReg):
    return (CMP, (REG, dstReg), (REG, srcReg))

def CMP_RegDisp_Reg(dstReg, disp, srcReg):
    return (CMP, (MEM, (REG, dstReg), disp), (REG, srcReg))

def JE_Label(label):
    return (JE, label)

def JNE_Label(label):
    return (JNE, label)

def JG_Label(label):
    return (JG,  label)

def JMP_label(label):
    return (JMP, label)

def ASM_LABEL(label):
    return (LABEL, label)

def CALL_Name(name):
    return (CALL, name)

def ASM_RET():
    return (RET,)

def ir_inst_to_str(i):
  def operand_to_str(op):
      if type(op) == tuple:
          if op[0] == REG: 
              if op[1] >= VIRTUAL_REG_BEGIN:
                  return '(%s, %d)' % (OPERAND2STR[op[0]], op[1])
              else:
                  return '(%s, %s)' % (OPERAND2STR[op[0]], PHY_REG2STR[op[1]])
          else:
              _s=[OPERAND2STR[op[0]]]
              for c in op[1:]:
                  _s.append(operand_to_str(c))
              return "(%s)" % ", ".join(_s)
      elif type(op) == str:
          return '"%s"' % op
      else:
          return '%s' % op
  if len(i) == 1:
      return "(%s,)" % (OPCODE2STR[i[0]])
  else:
      s=[OPCODE2STR[i[0]]]
      for op in i[1:]:
          s.append(operand_to_str(op))
      return "(%s)" % ', '.join(s)

def irs_print(irs):
    print("[")
    for ir in irs:
        ir_print(ir)
    print("]")

def ir_print(ir):
    print("[")
    for i in ir:
        print("  %s," % (ir_inst_to_str(i)))
    print("],")

# See http://en.wikibooks.org/wiki/X86_Assembly
def ir_print_in_gas(ir):
    for i in ir:
        if i[0] in [LABEL, PROLOGUE]:
            print("%s" % ir_inst2gas(i))
        else:
            print("      %s" % ir_inst2gas(i))

def ir_inst2gas(i):
    def ir_asm_operand(op):
        if type(op) == tuple:
            if op[0] == REG: 
                if op[1] >= VIRTUAL_REG_BEGIN:
                    return "%%r%d" % op[1]
                else:
                    return "%s" % NAMES[op[1]]
            elif op[0] == MEM:
                rop=op[1]
                disp=op[2]
                return "%d(%s)" % (disp, ir_asm_operand(rop))
            elif op[0] == IMM:
                return "$%d" % (op[1])
            else:
                return "%s" % op
        else:
            assert False
    if i[0] == MOV:
        return "mov %s, %s" % (
            ir_asm_operand(i[2]),
            ir_asm_operand(i[1]))
    elif i[0] == PUSH:
        return "push %s" % (
            ir_asm_operand(i[1])
            )
    elif i[0] == POP:
        return "pop %s" % (
            ir_asm_operand(i[1])
            )
    elif i[0] == CMP:
        return "cmp %s, %s" % (
            ir_asm_operand(i[2]),
            ir_asm_operand(i[1]))
    elif i[0] == JE:
        return "je .L%d" % (i[1])
    elif i[0] == JLE:
        return "jle .L%d" % (i[1])
    elif i[0] == JL:
        return "jl .L%d" % (i[1])
    elif i[0] == JG:
        return "jg .L%d" % (i[1])
    elif i[0] == JNE:
        return "jne .L%d" % (i[1])
    elif i[0] == LABEL:
        return ".L%d:" % i[1]
    elif i[0] == SUB:
        return "sub %s, %s" % (
            ir_asm_operand(i[2]),
            ir_asm_operand(i[1]))
    elif i[0] == ADD:
        return "add %s, %s" % (
            ir_asm_operand(i[2]),
            ir_asm_operand(i[1]))
    elif i[0] == CALL:
        return "call %s" % (
            i[1]
            )
    elif i[0] == RET:
        return "ret"
    elif i[0] == LEAVE:
        return "leave"
    elif i[0] == JMP:
        return "jmp .L%d" % (i[1])
    elif i[0] == PROLOGUE:
        return "%s: push %%ebp; mov  %%esp, %%ebp; sub  $%s, %%esp" \
            % (i[1], i[2])        
    else:
        return "TBI: %s" % ir_inst_to_str(i)

def irs_print(irs):
    for ir in irs:
        for i in ir:
            if i[0] in [LABEL, PROLOGUE]:
                print("%s" % ir_inst2gas(i))
            else:
                print("      %s" % ir_inst2gas(i))


M_MOVE, \
M_PLUS, \
M_MINUS, \
M_CONST, \
M_TEMP, \
M_MEM, \
M_NE, \
M_EQ, \
M_GT, \
M_CALL, \
=range(10)

MTREE_TYPE_STR={
  M_MOVE : "M_MOVE",
  M_PLUS : "M_PLUS",
  M_MINUS : "M_MINUS",
  M_CONST : "M_CONST",
  M_TEMP : "M_TEMP",
  M_MEM : "M_MEM",
  M_NE : "M_NE",
  M_EQ : "M_EQ",
  M_GT : "M_GT",
  M_CALL : "M_CALL",
}

def mtree2str(mtree):
    if type(mtree) == tuple:
        comp=['%s' % MTREE_TYPE_STR[mtree[0]]]
        for c in mtree[1:]:
            comp.append(mtree2str(c))
        return "(%s)" % ', '.join(comp)
    else:
        return '%s' % mtree

def cast_estmt2mtree(estmt):
    assert cast_get_node_type(estmt) == CAST_EXPR_STMT
    var_node=cast_get_child(estmt,0)
    binding=cast_get_attribute(var_node, 'binding')
    assert binding[0] == BINDING_VARIABLE
    offset=binding[1]
    rhs=cast_expr2mtree(cast_get_child(estmt,1))
    return (M_MOVE, (M_MEM, (M_PLUS, (M_TEMP, EBP), (M_CONST, offset))), rhs)

def cast_expr2mtree(expr):
    global p_count
    OP_CAST2MTREE={
        CAST_NOT_EQ_EXPR: M_NE,
        CAST_GREATER_EXPR: M_GT,
        CAST_MINUS_EXPR: M_MINUS,
        CAST_EQ_EXPR: M_EQ,
        }
    ttype=cast_get_node_type(expr)
    if ttype == CAST_VAR_EXPR:
        binding=cast_get_attribute(expr, 'binding')
        assert binding[0] == BINDING_VARIABLE
        offset=binding[1]
        return (M_MEM, (M_PLUS, (M_TEMP, EBP), (M_CONST, offset)))
    elif ttype in OP_CAST2MTREE:
        return (OP_CAST2MTREE[ttype], 
                cast_expr2mtree(cast_get_child(expr,0)), 
                cast_expr2mtree(cast_get_child(expr,1)))
    elif ttype == CAST_CALL_EXPR:
        fname=cast_get_attribute(expr, 'fname')
        l=[M_CALL, fname]
        for c in cast_get_children(expr):
            l.append(cast_expr2mtree(c))
        return tuple(l)
    elif ttype == CAST_INT_CONST_EXPR:
        value=cast_get_attribute(expr, 'value')
        return (M_CONST, value)
    else:
        assert False, "TBI: %s" % (CAST_NODE_STR[ttype])

def ir_build(translationUnit):
    translationUnitInfo=[
        0, # next_label_id
        ]
    def new_label_id():
        label_id=translationUnitInfo[0]
        translationUnitInfo[0] += 1
        return label_id
    irs=[]
    def ir_build_function(fdef):
        ir=[]
        functionInfo=[
            None, # exit_label_id
            cast_get_attribute(fdef, 'binding')[2], # frame_size
            0, # num_temp_variables 
            ]
        def set_exit_label_id(lid):
            functionInfo[0] = lid
        def get_exit_label_id():
            return functionInfo[0]
        def new_spill_slot():
            functionInfo[1] += 4
            slot = functionInfo[1]
            return - slot
        def new_virtual_reg_id():
            reg=functionInfo[2]
            functionInfo[2] += 1
            return reg + VIRTUAL_REG_BEGIN
        def get_frame_size():
            return functionInfo[1]
        def ir_append(*inst):
            for i in inst:
                ir.append(i)
        def build_stmt(n):
            if cast_get_node_type(n) == CAST_COMP_STMT:
                build_stmt(cast_get_child(n, 1))
            elif cast_get_node_type(n) == CAST_EXPR_STMT:
                build_expr_stmt(n)
            elif cast_get_node_type(n) == CAST_STMT_LIST:
                for c in cast_get_children(n):
                    build_stmt(c)
            elif cast_get_node_type(n) in [CAST_EQ_EXPR,CAST_VAR_EXPR,CAST_NOT_EQ_EXPR,CAST_GREATER_EXPR,CAST_PLUS_EXPR, CAST_MINUS_EXPR,CAST_CALL_EXPR]:
                return build_expr(n)
            elif cast_get_node_type(n) == CAST_IF_STMT:
                build_expr(cast_get_child(n, 0))
                L1 = new_label_id()
                functionInfo[2] -= 1
                r = new_virtual_reg_id()
                ir_append(CMP_Reg_imm(r, 0), JE_Label(L1))
                L2 = new_label_id()
                build_stmt(cast_get_child(n, 1))
                ir_append(JMP_label(L2), ASM_LABEL(L1))
                build_stmt(cast_get_child(n, 2))
                ir_append(ASM_LABEL(L2))
            elif cast_get_node_type(n) == CAST_WHILE_STMT:
                L1 = new_label_id()
                L2 = new_label_id()
                ir_append(ASM_LABEL(L1))
                build_expr(cast_get_child(n, 0))
                functionInfo[2] -= 1
                r = new_virtual_reg_id()
                ir_append(CMP_Reg_imm(r,0), JE_Label(L2))
                for c in cast_get_children(n)[1:]:
                    build_stmt(c)
                ir_append(JMP_label(L1), (ASM_LABEL(L2)))
            elif cast_get_node_type(n) == CAST_RETURN_STMT:
                r = build_expr(cast_get_child(n,0))
                for c in cast_get_children(n)[1:]:
                    build_stmt(c)
                ir_append(MOV_Reg_Reg(EAX, r), JMP_label(lexit))
            else:
                TBI()
        def build_expr_stmt(estmt):
            mtree=cast_estmt2mtree(estmt)
            mtree_munch_move(mtree)
        def build_expr(expr):
            mtree=cast_expr2mtree(expr)
            r=mtree_munch_expr(mtree)
            return r
        def mtree_munch_move(mtree):
            assert mtree[0] == M_MOVE
            assert mtree[1][0] == M_MEM
            if mtree[2][0] == M_MINUS and mtree[1][1][2][0] == M_CONST and mtree[2][1][0] == M_MEM and mtree[2][1][1][0] == M_PLUS and mtree[2][1][1][2][0] == M_CONST and mtree[2][2][0] == M_MEM and mtree[2][2][1][0] == M_PLUS and mtree[2][2][1][2][0] == M_CONST: # Munch Node Number : 11
                r = new_virtual_reg_id()
                ir_append(
                    MOV_Reg_RegDisp(r,mtree[1][1][1][1],mtree[2][2][1][2][1]),
                    SUB_RegDisp_Reg(mtree[2][1][1][1][1],mtree[2][1][1][2][1],r),
                )
            elif mtree[1][1][0] == M_PLUS and mtree[1][1][2][0] == M_CONST and mtree[2][0] == M_CALL and mtree[2][2][0] == M_CONST and mtree[2][3][0] == M_CONST: # Munch Node Number : 7
                rlhs = mtree_munch_expr(mtree[1][1])
                rrhs = mtree_munch_expr(mtree[2])
                ir_append(MOV_RegDisp_Reg(mtree[1][1][1][1], mtree[1][1][2][1], rrhs))
        def mtree_munch_expr(mt):
            if mt[0] == M_NE and mt[1][0] == M_MEM and mt[2][0] == M_MEM and mt[1][1][0] == M_PLUS and mt[1][1][2][0] == M_CONST and mt[2][1][0] == M_PLUS and mt[2][1][2][0] == M_CONST: # Munch Node Number : 7
                r4=new_virtual_reg_id()
                r3=new_virtual_reg_id()
                l=new_label_id()
                ir_append(
                    MOV_Reg_RegDisp(r4, mt[1][1][1][1], mt[2][1][2][1]),
                    MOV_Reg_Imm(r3, 1),
                    CMP_RegDisp_Reg(mt[1][1][1][1], mt[1][1][2][1], r4),
                    JNE_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                    )
                return r3

            elif mt[0] == M_EQ and mt[1][0] == M_MEM and mt[2][0] == M_MEM and mt[1][1][0] == M_PLUS and mt[1][1][2][0] == M_CONST and mt[2][1][0] == M_PLUS and mt[2][1][2][0] == M_CONST: #Munch Node Number : 7
                r4 = new_virtual_reg_id()
                r3 = new_virtual_reg_id()
                l = new_label_id()
                ir_append(
                    MOV_Reg_RegDisp(r4, mt[1][1][1][1], mt[2][1][2][1]),
                    MOV_Reg_Imm(r3, 1),
                    CMP_RegDisp_Reg(mt[1][1][1][1], mt[1][1][2][1], r4),
                    JE_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                )
                return r3
            elif mt[0] == M_GT and mt[1][0] == M_MEM and mt[2][0] == M_MEM and mt[1][1][0] == M_PLUS and mt[1][1][2][0] == M_CONST and mt[2][1][0] == M_PLUS and mt[2][1][2][0] == M_CONST: #Munch Node Number : 7
                r4 = new_virtual_reg_id()
                r3 = new_virtual_reg_id()
                l = new_label_id()
                ir_append(
                    MOV_Reg_RegDisp(r4, mt[1][1][1][1], mt[2][1][2][1]),
                    MOV_Reg_Imm(r3, 1),
                    CMP_RegDisp_Reg(mt[1][1][1][1], mt[1][1][2][1], r4),
                    JG_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                )
                return r3
            elif mt[0] == M_MEM and mt[1][0] == M_PLUS and mt[1][1][0] == M_TEMP and mt[1][2][0] == M_CONST: # Munch Node Number : 3
                r = new_virtual_reg_id()
                ir_append(MOV_Reg_RegDisp(r, mt[1][1][1], mt[1][2][1]))
                return r
            elif mt[0] == M_PLUS and mt[1][0] == M_TEMP and mt[2][0] == M_CONST: #Munch Node Number : 2
                functionInfo[2]-=1
                r = new_virtual_reg_id()
                return r
            elif mt[0] == M_NE:
                print (mt)
                r1=mtree_munch_expr(mt[1])
                r2=mtree_munch_expr(mt[2])
                r3=new_virtual_reg_id()
                l=new_label_id()
                ir_append(
                    MOV_Reg_Imm(r3, 1),
                    CMP_Reg_Reg(r1, r2),
                    JNE_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                    )
                return r3     
            elif mt[0] == M_EQ:
                r1=mtree_munch_expr(mt[1])
                r2=mtree_munch_expr(mt[2])
                r3=new_virtual_reg_id()
                l=new_label_id()
                ir_append(
                    MOV_Reg_Imm(r3, 1),
                    CMP_Reg_Reg(r1,r2),
                    JE_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                    )
                return r3
            elif mt[0] == M_GT:
                r1=mtree_munch_expr(mt[1])
                r2=mtree_munch_expr(mt[2])
                r3=new_virtual_reg_id()
                l=new_label_id()
                ir_append(
                    MOV_Reg_Imm(r3, 1),
                    CMP_Reg_Reg(r1,r2),
                    JG_Label(l),
                    MOV_Reg_Imm(r3, 0),
                    ASM_LABEL(l),
                    )
                return r3
            elif mt[0] == M_MEM:
                r1=mtree_munch_expr(mt[1])
                r2=new_virtial_reg_id()
                ir_append(
                    MOV_Reg_RegDisp(r2, r1, 0)
                    )
                return r2
            elif mt[0] == M_TEMP:
                reg=mt[1]
                return reg
            elif mt[0] == M_PLUS:
                r1=mtree_munch_expr(mt[1])
                r2=mtree_munch_expr(mt[2])
                r3=new_virtual_reg_id()
                ir_append(
                    MOV_Reg_Reg(r3, r1),
                    ADD_Reg_Reg(r3, r2),
                    )
                return r3
            elif mt[0] == M_MINUS:
                r1=mtree_munch_expr(mt[1])
                r2=mtree_munch_expr(mt[2])
                r3=new_virtual_reg_id()
                ir_append(
                    MOV_Reg_Reg(r3,r1),
                    SUB_Reg_Reg(r3,r2),
                    )
                return r3
            elif mt[0] == M_CONST:
                imm=mt[1]
                r=new_virtual_reg_id()
                ir_append(
                    MOV_Reg_Imm(r, imm)
                    )
                return r
            elif mt[0] == M_CALL:
                fname=mt[1]
                pregs=[]
                for c in mt[2:]:
                    r=mtree_munch_expr(c)
                    pregs.append(r)
                for pr in reversed(pregs):
                    ir_append(
                        PUSH_Reg(pr)
                        )
                arg_size=4 * len(pregs)
                ir_append(
                    CALL_Name(fname),
                    ADD_Reg_Imm(ESP, arg_size)
                    )
                return EAX
            else:
                assert False,"TBI: %s" % MTREE_TYPE_STR[mt[0]]
            assert False, 'Unreachable'
        assert cast_get_node_type(fdef) == CAST_FUN_DEFINITION
        fname=cast_get_attribute(fdef, 'id')
        ir_append(
            None # Place holder for the prologue instruction
            )
        spillLocation={}
        for r in NONVOLATILE_REGISTERS:
            t=new_spill_slot()
            spillLocation[r]=t
            ir_append(
                MOV_RegDisp_Reg(EBP, t, r)
                )
        lexit=new_label_id()
        set_exit_label_id(lexit)
        build_stmt(cast_get_child(fdef, 1))
        ir_append(
            ASM_LABEL(lexit)
            )
        for r in NONVOLATILE_REGISTERS:
            t=spillLocation[r]
            ir_append(
                MOV_Reg_RegDisp(r, EBP, t)
                )
        ir_append(
            MOV_Reg_Reg(ESP, EBP),
            POP_Reg(EBP),
            ASM_RET()
            )
        frameSize=get_frame_size()
        ir[0]=(PROLOGUE, fname, get_frame_size())
        return ir
    assert cast_get_node_type(translationUnit) == CAST_TRANSLATION_UNIT
    for c in cast_get_children(translationUnit):
        ir=ir_build_function(c)
        irs.append(ir)
    return irs

INPUT_AST= \
[CAST_TRANSLATION_UNIT, {},
  [CAST_FUN_DEFINITION, {'id': "gcd"},
    [CAST_PAR_TYPE_LIST, {},
      [CAST_PAR_TYPE, {'id': "a"}],
      [CAST_PAR_TYPE, {'id': "b"}],
    ],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {}],
      [CAST_STMT_LIST, {},
        [CAST_WHILE_STMT, {},
          [CAST_NOT_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'id': "a"}],
            [CAST_VAR_EXPR, {'id': "b"}],
          ],
          [CAST_COMP_STMT, {},
            [CAST_DECL_LIST, {}],
            [CAST_STMT_LIST, {},
              [CAST_IF_STMT, {},
                [CAST_GREATER_EXPR, {},
                  [CAST_VAR_EXPR, {'id': "a"}],
                  [CAST_VAR_EXPR, {'id': "b"}],
                ],
                [CAST_EXPR_STMT, {},
                  [CAST_VAR_EXPR, {'id': "a"}],
                  [CAST_MINUS_EXPR, {},
                    [CAST_VAR_EXPR, {'id': "a"}],
                    [CAST_VAR_EXPR, {'id': "b"}],
                  ],
                ],
                [CAST_EXPR_STMT, {},
                  [CAST_VAR_EXPR, {'id': "b"}],
                  [CAST_MINUS_EXPR, {},
                    [CAST_VAR_EXPR, {'id': "b"}],
                    [CAST_VAR_EXPR, {'id': "a"}],
                  ],
                ],
              ],
            ],
          ],
        ],
        [CAST_RETURN_STMT, {},
          [CAST_VAR_EXPR, {'id': "a"}],
        ],
      ],
    ],
  ],
  [CAST_FUN_DEFINITION, {'id': "rgcd"},
    [CAST_PAR_TYPE_LIST, {},
      [CAST_PAR_TYPE, {'id': "a"}],
      [CAST_PAR_TYPE, {'id': "b"}],
    ],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {}],
      [CAST_STMT_LIST, {},
        [CAST_IF_STMT, {},
          [CAST_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'id': "a"}],
            [CAST_VAR_EXPR, {'id': "b"}],
          ],
          [CAST_COMP_STMT, {},
            [CAST_DECL_LIST, {}],
            [CAST_STMT_LIST, {},
              [CAST_RETURN_STMT, {},
                [CAST_VAR_EXPR, {'id': "a"}],
              ],
            ],
          ],
          [CAST_IF_STMT, {},
            [CAST_GREATER_EXPR, {},
              [CAST_VAR_EXPR, {'id': "a"}],
              [CAST_VAR_EXPR, {'id': "b"}],
            ],
            [CAST_COMP_STMT, {},
              [CAST_DECL_LIST, {}],
              [CAST_STMT_LIST, {},
                [CAST_RETURN_STMT, {},
                  [CAST_CALL_EXPR, {'fname': "rgcd"},
                    [CAST_MINUS_EXPR, {},
                      [CAST_VAR_EXPR, {'id': "a"}],
                      [CAST_VAR_EXPR, {'id': "b"}],
                    ],
                    [CAST_VAR_EXPR, {'id': "b"}],
                  ],
                ],
              ],
            ],
            [CAST_COMP_STMT, {},
              [CAST_DECL_LIST, {}],
              [CAST_STMT_LIST, {},
                [CAST_RETURN_STMT, {},
                  [CAST_CALL_EXPR, {'fname': "rgcd"},
                    [CAST_VAR_EXPR, {'id': "a"}],
                    [CAST_MINUS_EXPR, {},
                      [CAST_VAR_EXPR, {'id': "b"}],
                      [CAST_VAR_EXPR, {'id': "a"}],
                    ],
                  ],
                ],
              ],
            ],
          ],
        ],
      ],
    ],
  ],
  [CAST_FUN_DEFINITION, {'id': "main"},
    [CAST_PAR_TYPE_LIST, {}],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {},
        [CAST_VAR_DECLARATION, {'id': "g1"}],
        [CAST_VAR_DECLARATION, {'id': "g2"}],
      ],
      [CAST_STMT_LIST, {},
        [CAST_EXPR_STMT, {},
          [CAST_VAR_EXPR, {'id': "g1"}],
          [CAST_CALL_EXPR, {'fname': "gcd"},
            [CAST_INT_CONST_EXPR, {'value': 815}],
            [CAST_INT_CONST_EXPR, {'value': 625}],
          ],
        ],
        [CAST_EXPR_STMT, {},
          [CAST_VAR_EXPR, {'id': "g2"}],
          [CAST_CALL_EXPR, {'fname': "rgcd"},
            [CAST_INT_CONST_EXPR, {'value': 815}],
            [CAST_INT_CONST_EXPR, {'value': 625}],
          ],
        ],
        [CAST_RETURN_STMT, {},
          [CAST_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'id': "g1"}],
            [CAST_VAR_EXPR, {'id': "g2"}],
          ],
        ],
      ],
    ],
  ],
]

OUTPUT_AST= \
[CAST_TRANSLATION_UNIT, {},
  [CAST_FUN_DEFINITION, {'binding': [0, 'gcd', 0], 'id': "gcd"},
    [CAST_PAR_TYPE_LIST, {},
      [CAST_PAR_TYPE, {'binding': [1, 8], 'id': "a"}],
      [CAST_PAR_TYPE, {'binding': [1, 12], 'id': "b"}],
    ],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {}],
      [CAST_STMT_LIST, {},
        [CAST_WHILE_STMT, {},
          [CAST_NOT_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
            [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
          ],
          [CAST_COMP_STMT, {},
            [CAST_DECL_LIST, {}],
            [CAST_STMT_LIST, {},
              [CAST_IF_STMT, {},
                [CAST_GREATER_EXPR, {},
                  [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                  [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                ],
                [CAST_EXPR_STMT, {},
                  [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                  [CAST_MINUS_EXPR, {},
                    [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                    [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                  ],
                ],
                [CAST_EXPR_STMT, {},
                  [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                  [CAST_MINUS_EXPR, {},
                    [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                    [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                  ],
                ],
              ],
            ],
          ],
        ],
        [CAST_RETURN_STMT, {},
          [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
        ],
      ],
    ],
  ],
  [CAST_FUN_DEFINITION, {'binding': [0, 'rgcd', 0], 'id': "rgcd"},
    [CAST_PAR_TYPE_LIST, {},
      [CAST_PAR_TYPE, {'binding': [1, 8], 'id': "a"}],
      [CAST_PAR_TYPE, {'binding': [1, 12], 'id': "b"}],
    ],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {}],
      [CAST_STMT_LIST, {},
        [CAST_IF_STMT, {},
          [CAST_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
            [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
          ],
          [CAST_COMP_STMT, {},
            [CAST_DECL_LIST, {}],
            [CAST_STMT_LIST, {},
              [CAST_RETURN_STMT, {},
                [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
              ],
            ],
          ],
          [CAST_IF_STMT, {},
            [CAST_GREATER_EXPR, {},
              [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
              [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
            ],
            [CAST_COMP_STMT, {},
              [CAST_DECL_LIST, {}],
              [CAST_STMT_LIST, {},
                [CAST_RETURN_STMT, {},
                  [CAST_CALL_EXPR, {'binding': [0, 'rgcd', 0], 'fname': "rgcd"},
                    [CAST_MINUS_EXPR, {},
                      [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                      [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                    ],
                    [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                  ],
                ],
              ],
            ],
            [CAST_COMP_STMT, {},
              [CAST_DECL_LIST, {}],
              [CAST_STMT_LIST, {},
                [CAST_RETURN_STMT, {},
                  [CAST_CALL_EXPR, {'binding': [0, 'rgcd', 0], 'fname': "rgcd"},
                    [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                    [CAST_MINUS_EXPR, {},
                      [CAST_VAR_EXPR, {'binding': [1, 12], 'id': "b"}],
                      [CAST_VAR_EXPR, {'binding': [1, 8], 'id': "a"}],
                    ],
                  ],
                ],
              ],
            ],
          ],
        ],
      ],
    ],
  ],
  [CAST_FUN_DEFINITION, {'binding': [0, 'main', 8], 'id': "main"},
    [CAST_PAR_TYPE_LIST, {}],
    [CAST_COMP_STMT, {},
      [CAST_DECL_LIST, {},
        [CAST_VAR_DECLARATION, {'binding': [1, -4], 'id': "g1"}],
        [CAST_VAR_DECLARATION, {'binding': [1, -8], 'id': "g2"}],
      ],
      [CAST_STMT_LIST, {},
        [CAST_EXPR_STMT, {},
          [CAST_VAR_EXPR, {'binding': [1, -4], 'id': "g1"}],
          [CAST_CALL_EXPR, {'binding': [0, 'gcd', 0], 'fname': "gcd"},
            [CAST_INT_CONST_EXPR, {'value': 815}],
            [CAST_INT_CONST_EXPR, {'value': 625}],
          ],
        ],
        [CAST_EXPR_STMT, {},
          [CAST_VAR_EXPR, {'binding': [1, -8], 'id': "g2"}],
          [CAST_CALL_EXPR, {'binding': [0, 'rgcd', 0], 'fname': "rgcd"},
            [CAST_INT_CONST_EXPR, {'value': 815}],
            [CAST_INT_CONST_EXPR, {'value': 625}],
          ],
        ],
        [CAST_RETURN_STMT, {},
          [CAST_EQ_EXPR, {},
            [CAST_VAR_EXPR, {'binding': [1, -4], 'id': "g1"}],
            [CAST_VAR_EXPR, {'binding': [1, -8], 'id': "g2"}],
          ],
        ],
      ],
    ],
  ],
]

OUTPUT_IRS= \
[
[
  (PROLOGUE, "gcd", 12),
  (MOV, (MEM, (REG, EBP), -4), (REG, EBX)),
  (MOV, (MEM, (REG, EBP), -8), (REG, ESI)),
  (MOV, (MEM, (REG, EBP), -12), (REG, EDI)),
  (LABEL, 1),
  (MOV, (REG, 8), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 9), (IMM, 1)),
  (CMP, (MEM, (REG, EBP), 8), (REG, 8)),
  (JNE, 3),
  (MOV, (REG, 9), (IMM, 0)),
  (LABEL, 3),
  (CMP, (REG, 9), (IMM, 0)),
  (JE, 2),
  (MOV, (REG, 10), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 11), (IMM, 1)),
  (CMP, (MEM, (REG, EBP), 8), (REG, 10)),
  (JG, 4),
  (MOV, (REG, 11), (IMM, 0)),
  (LABEL, 4),
  (CMP, (REG, 11), (IMM, 0)),
  (JE, 5),
  (MOV, (REG, 12), (MEM, (REG, EBP), 12)),
  (SUB, (MEM, (REG, EBP), 8), (REG, 12)),
  (JMP, 6),
  (LABEL, 5),
  (MOV, (REG, 13), (MEM, (REG, EBP), 8)),
  (SUB, (MEM, (REG, EBP), 12), (REG, 13)),
  (LABEL, 6),
  (JMP, 1),
  (LABEL, 2),
  (MOV, (REG, 14), (MEM, (REG, EBP), 8)),
  (MOV, (REG, EAX), (REG, 14)),
  (JMP, 0),
  (LABEL, 0),
  (MOV, (REG, EBX), (MEM, (REG, EBP), -4)),
  (MOV, (REG, ESI), (MEM, (REG, EBP), -8)),
  (MOV, (REG, EDI), (MEM, (REG, EBP), -12)),
  (MOV, (REG, ESP), (REG, EBP)),
  (POP, (REG, EBP)),
  (RET,),
],
[
  (PROLOGUE, "rgcd", 12),
  (MOV, (MEM, (REG, EBP), -4), (REG, EBX)),
  (MOV, (MEM, (REG, EBP), -8), (REG, ESI)),
  (MOV, (MEM, (REG, EBP), -12), (REG, EDI)),
  (MOV, (REG, 8), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 9), (IMM, 1)),
  (CMP, (MEM, (REG, EBP), 8), (REG, 8)),
  (JE, 8),
  (MOV, (REG, 9), (IMM, 0)),
  (LABEL, 8),
  (CMP, (REG, 9), (IMM, 0)),
  (JE, 9),
  (MOV, (REG, 10), (MEM, (REG, EBP), 8)),
  (MOV, (REG, EAX), (REG, 10)),
  (JMP, 7),
  (JMP, 10),
  (LABEL, 9),
  (MOV, (REG, 11), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 12), (IMM, 1)),
  (CMP, (MEM, (REG, EBP), 8), (REG, 11)),
  (JG, 11),
  (MOV, (REG, 12), (IMM, 0)),
  (LABEL, 11),
  (CMP, (REG, 12), (IMM, 0)),
  (JE, 12),
  (MOV, (REG, 13), (MEM, (REG, EBP), 8)),
  (MOV, (REG, 14), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 15), (REG, 13)),
  (SUB, (REG, 15), (REG, 14)),
  (MOV, (REG, 16), (MEM, (REG, EBP), 12)),
  (PUSH, (REG, 16)),
  (PUSH, (REG, 15)),
  (CALL, "rgcd"),
  (ADD, (REG, ESP), (IMM, 8)),
  (MOV, (REG, EAX), (REG, EAX)),
  (JMP, 7),
  (JMP, 13),
  (LABEL, 12),
  (MOV, (REG, 17), (MEM, (REG, EBP), 8)),
  (MOV, (REG, 18), (MEM, (REG, EBP), 12)),
  (MOV, (REG, 19), (MEM, (REG, EBP), 8)),
  (MOV, (REG, 20), (REG, 18)),
  (SUB, (REG, 20), (REG, 19)),
  (PUSH, (REG, 20)),
  (PUSH, (REG, 17)),
  (CALL, "rgcd"),
  (ADD, (REG, ESP), (IMM, 8)),
  (MOV, (REG, EAX), (REG, EAX)),
  (JMP, 7),
  (LABEL, 13),
  (LABEL, 10),
  (LABEL, 7),
  (MOV, (REG, EBX), (MEM, (REG, EBP), -4)),
  (MOV, (REG, ESI), (MEM, (REG, EBP), -8)),
  (MOV, (REG, EDI), (MEM, (REG, EBP), -12)),
  (MOV, (REG, ESP), (REG, EBP)),
  (POP, (REG, EBP)),
  (RET,),
],
[
  (PROLOGUE, "main", 20),
  (MOV, (MEM, (REG, EBP), -12), (REG, EBX)),
  (MOV, (MEM, (REG, EBP), -16), (REG, ESI)),
  (MOV, (MEM, (REG, EBP), -20), (REG, EDI)),
  (MOV, (REG, 8), (IMM, 815)),
  (MOV, (REG, 9), (IMM, 625)),
  (PUSH, (REG, 9)),
  (PUSH, (REG, 8)),
  (CALL, "gcd"),
  (ADD, (REG, ESP), (IMM, 8)),
  (MOV, (MEM, (REG, EBP), -4), (REG, EAX)),
  (MOV, (REG, 10), (IMM, 815)),
  (MOV, (REG, 11), (IMM, 625)),
  (PUSH, (REG, 11)),
  (PUSH, (REG, 10)),
  (CALL, "rgcd"),
  (ADD, (REG, ESP), (IMM, 8)),
  (MOV, (MEM, (REG, EBP), -8), (REG, EAX)),
  (MOV, (REG, 12), (MEM, (REG, EBP), -8)),
  (MOV, (REG, 13), (IMM, 1)),
  (CMP, (MEM, (REG, EBP), -4), (REG, 12)),
  (JE, 15),
  (MOV, (REG, 13), (IMM, 0)),
  (LABEL, 15),
  (MOV, (REG, EAX), (REG, 13)),
  (JMP, 14),
  (LABEL, 14),
  (MOV, (REG, EBX), (MEM, (REG, EBP), -12)),
  (MOV, (REG, ESI), (MEM, (REG, EBP), -16)),
  (MOV, (REG, EDI), (MEM, (REG, EBP), -20)),
  (MOV, (REG, ESP), (REG, EBP)),
  (POP, (REG, EBP)),
  (RET,),
],
]


def main():
    print("### INPUT AST ###")
    cast_dump(INPUT_AST)
    print("### EXPECTED OUTPUT AST ###")
    cast_dump(OUTPUT_AST)

    ast=INPUT_AST
    cast_analyze(ast)

    print("### OUTPUT AST ###")
    cast_dump(ast)

    print("### EXPECTED IR ###")
    irs_print(OUTPUT_IRS)
    print("### OUTPUT IR ###")
    irs_out=ir_build(OUTPUT_AST)
    irs_print(irs_out)

    print("%-10s ASTAnalysis" % ("SUCCESS" if ast == OUTPUT_AST else "FAIL"))
    print("%-10s AST2IR" % ("SUCCESS" if irs_out == OUTPUT_IRS else "FAIL"))

if __name__ == "__main__":
    main()
