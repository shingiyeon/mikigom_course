#!/usr/bin/python3
import sys
import subprocess
import os
import inspect

def TBI():
    print("WRANING: TBI in %s at %s:%d" % (
            inspect.currentframe().f_back.f_code.co_name,
            inspect.currentframe().f_back.f_code.co_filename,
            inspect.currentframe().f_back.f_lineno))


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

REGISTERS_FOR_ALLOCATION=set([
        EAX, ECX, EDX, 
        EBX, ESI ,EDI,
])


INPUT_IRS= \
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

# See http://en.wikibooks.org/wiki/X86_Assembly
def irs_print_in_gas(irs):
    for ir in irs:
        ir_print_in_gas(ir)

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

def ir_inst_get_use_def(inst):
    def op2regs(op):
        regs=set()
        if op[0] == REG:
            regs.add(op[1])
        elif op[0] == MEM:
            if op[1] != None:
                regs.add(op[1][1])
        return regs
    def operand_mem_get_regs(mop):
        regs=set()
        assert mop[0] == MEM
        if mop[1] != None:
            regs.add(mop[1][1])
        return regs
    opcode=inst[0]
    uses=set()
    defs=set()
    if opcode == MOV:
        op0=inst[1]
        if op0[0] == REG:
            defs |= op2regs(op0)
        else:
            uses |= op2regs(op0)
        op1=inst[2]
        uses |= op2regs(op1)
    elif opcode == PUSH:
        uses |= op2regs(inst[1])
    elif opcode == POP: 
        if inst[1][0] == REG:
            defs |= op2regs(inst[1])
    elif opcode in [ADD, SUB]: 
        if inst[1][0] == REG:
            defs |= op2regs(inst[1])
            uses |= op2regs(inst[1])
        else:
            uses |= op2regs(inst[1])
        uses |= op2regs(inst[2])
    elif opcode == CMP: 
        uses |= op2regs(inst[1])
        uses |= op2regs(inst[2])
    elif opcode in [JMP,JE,JNE,JG,JGE, JLE, JL]: 
        pass
    elif opcode == CALL: 
        defs.add(EAX)
    elif opcode == RET:
        uses.add(EAX)
    elif opcode == LEAVE:
        pass
    elif opcode == LABEL: 
        pass
    elif opcode == PROLOGUE: 
        pass
    else: 
        assert False, "TBI: %s" % OPCODE2STR[opcode]
    return uses,defs

def ir_inst_get_succs(ir):
    succs={}
    label_map={}
    for i in range(len(ir)):
        succs[i]=set()
        inst=ir[i]
        if inst[0] == LABEL:
            label_index=inst[1]
            label_map[label_index]=i
    for i in range(len(ir)):
        inst=ir[i]
        opcode=inst[0]
        if opcode in [ JE, 
            JNE, JG,
            JGE]:
            label_index=inst[1]
            target=label_map[label_index]
            succs[i].add(target)
            succs[i].add(i+1)
        elif opcode == JMP:
            succs[i].add(target)
        elif opcode == RET:
            pass
        else:
            if (i + 1) < len(ir):
                succs[i].add(i+1)
    return succs

def ir_reg_alloc(ir):
    succs=ir_inst_get_succs(ir)
    uses={}
    defs={}
    live_in={}
    live_out={}
    live_in_prime={}
    live_out_prime={}
    for i in range(len(ir)):
        uses[i],defs[i]=ir_inst_get_use_def(ir[i])
        live_in[i]=set()
        live_out[i]=set()
        live_in_prime[i]=set()
        live_out_prime[i]=set()
    def liveness_analysis():
        while True:
            for i in range(len(ir)):
                live_in_prime[i] = live_in[i]
                live_out_prime[i] = live_out[i]
                live_in[i] = uses[i]|(live_out[i]-defs[i])
                for j in range(len(succs[i])):
                    live_out[i] = live_out[i]|live_in[list(succs[i])[j]]
            if live_in_prime == live_in and live_out_prime == live_out:
                break
    def liveness_print():
        print('%3s %-8s %-7s %-12s %-30s %-30s %s' % (
                'loc', 'succ', 'def', 'use', 'livein', 'liveout', 'instruction'))
        for i in range(len(ir)):
            def reg2str(reg):
                if reg >= VIRTUAL_REG_BEGIN:
                    return '%%r%d' % reg
                else:
                    return NAMES[reg]
            def regs2str(regs):
                return '{%s}' % ', '.join(map(lambda x: reg2str(x), regs))
            print('%3d %-8s %-7s %-12s %-30s %-30s %s' % (
                    i, '{%s}' % ', '.join(map(lambda x: '%d' % x , succs[i])),
                    regs2str(defs[i]), regs2str(uses[i]),
                    regs2str(live_in[i]), regs2str(live_out[i]),
                    ir_inst2gas(ir[i])))
        return live_out
    # a representation of an interference graph
    nodes=set()
    precolored=set()
    adjset=set()
    adjlist={}
    degree={}
    def ifgraph_add_node(n):
        if n not in nodes:
            nodes.add(n)
            adjlist[n]=set()
            degree[n]=0
            if n < VIRTUAL_REG_BEGIN:
                precolored.add(n)
    def ifgraph_add_edge(s, t):
        if s == t or (s,t) in adjset:
            return
        adjset.add((s,t))
        adjset.add((t,s))
        ifgraph_add_node(s)
        ifgraph_add_node(t)
        adjlist[s].add(t)
        degree[s] += 1
        adjlist[t].add(s)
        degree[t] += 1
    def ifgraph_adjacent(n, exclude=set()):
        r=set()
        for n in adjlist[n]:
            if n not in exclude:
                r.add(n)
        return r
    def ifgraph_to_dot(view=False,ofname=None):
        if ofname == None:
            fname=ir[0][1][1]
            ofname='%s.g' % fname
        with open(ofname, 'w') as f:
            print('graph {', file=f)
            for n in nodes:
                print(' r%d [label="r%d(%d)"];' % (n, n, degree[n]), file=f)
            for s,t in adjset:
                if s < t:
                    print('  r%d--r%d;' % (s,t), file =f)
            print('}',file=f)
        if view:
            subprocess.call('xdot %s' % ofname, shell=True)
    def build_interference_graph():
        for i in range(len(ir)):
            inst=ir[i]
            if inst[0] == CALL:
                for r in live_out[i]:
                    for v in VOLATILE_REGISTERS:
                        ifgraph_add_edge(r, v)
        for i in range(len(ir)):
            for j in range(len(list(defs[i]))):
                ifgraph_add_node(list(defs[i])[j])
            for j in range(len(list(live_out[i]))):
                ifgraph_add_node(list(live_out[i])[j])
        for i in range(len(ir)):
            for j in range(len(list(defs[i]))):
                for k in range(len(list(live_out[i]))):
                    ifgraph_add_edge(list(defs[i])[j], list(live_out[i])[k])
        ifgraph_to_dot(False)
# map from virtual registers to physical registers as a result of coloring
    color_map={}
    def simplify_and_select():
        K=len(REGISTERS_FOR_ALLOCATION)
#        print (K)
#        print (precolored)
#        print (REGISTERS_FOR_ALLOCATION)
        general_node = []
        for i in nodes:
            if i in precolored:
                color_map[i] = i
#        print ("color_map")
#        print (color_map)
        for i in range(len(precolored), len(nodes)):
            general_node.append(list(nodes)[i])

#        print ("nodes")
#        print (nodes)
#        print ("adjset")
#        print (adjset)
#        print ("adjlist")
#        print (adjlist)
#        print ("color_map")
#        print (color_map)

        G_neighbor = {}
        G_nodes = general_node
        colors_of_nodes={}

        for i in range(len(G_nodes)):
            G_neighbor[G_nodes[i]] = []

        for i in range(len(adjset)):
#            print ("G_neighbor")
#            print (G_neighbor)
            if list(adjset)[i][0] in G_nodes and list(adjset)[i][1] in G_nodes:
                G_neighbor[list(adjset)[i][0]].append(list(adjset)[i][1])

        def get_color_for_node(node):
            for color in REGISTERS_FOR_ALLOCATION:
                if coloring(node, color):
                    return color

        def coloring(node, color):
            for neighbor in G_neighbor[node]:
                color_of_neighbor = colors_of_nodes.get(neighbor, None)
                if color_of_neighbor == color:
                    return False
            return True

        for node in G_nodes:
            colors_of_nodes[node] = get_color_for_node(node)

        for i in range(len(G_nodes)):
            color_map[G_nodes[i]] = colors_of_nodes[G_nodes[i]]
 
#        now_node = list(nodes)[len(precolored)]
#        visited = [now_node]
#        node_stack.append(now_node)
#        i = 0
#        j = 0
#        to_colored_number = len(nodes) - len(precolored)
#        while True:
#            print (node_stack)
#            j += 1
#            if now_node == list(adjset)[i%len(adjset)][0] and list(adjset)[i%len(adjset)][1] not in visited:
#                now_node = list(adjset)[i%len(adjset)][1]
#                node_stack.append(now_node)
#                visited.append(now_node)
#            if len(node_stack) == len(nodes) - len(precolored):
#                break
#            i += 1
#            if j == to_colored_number:
#                j = 0
#                now_node == list(adjset)[(i+2)%len(adjset)][0]

 #       print ("p0recolored")
#        print (precolored)
#
#        print ("node_stack")
#        print (node_stack)
#        coloring_graph = {}
#        coloring = {}
#        colors_in_use = []
#        first_node = node_stack.pop()
#        coloring_graph[first_node] = []
#        coloring[first_node] = 0
#        colors_in_use.append(0)
#        print ("coloring_graph")
#        print (coloring_graph)
#        print ("coloring")
#        print (coloring)
#        print ("colors_in_use")
#        print (colors_in_use)
#        for i in range(1, len(node_stack)):
#            now_node = node_stack.pop()
#            now_color_searching = colors_in_use
#            coloring_graph[now_node] = []
#            print (coloring_graph)
#            for j in range(len(list(adjset))):
#                if now_node == list(adjset)[j][0] and list(adjset)[j][1] in coloring_graph.keys():
#                    coloring_graph[now_node] = list(adjset)[j][1]
#                    coloring_graph[list(adjset)[j][1]] = now_node
#                    now_color_searching.remove(coloring[list(adjset)[j][1]])
#            if len(now_color_searching) != 0:
#                 coloring[now_node] = now_color_searching[0]
#            else:
#                 print ("colors_in_use")
#                 print (colors_in_use)
#                 colors_in_use.append(colors_in_use[-1]+1)
#                 coloring[now_node] = colors_in_use[-1]

            
#        for i in range(len(1, node_stack)):
#            color_searching = colors_in_use
#            now_node = node_stack.pop()
#            for j in range(len(list(adjset))):
#                if(now_node==list(adjset)[j][0] and list(adjset)[j][1] in coloring_graph.key()):
#                    color_searching.remove(coloring[list(adjset)[j][1]])
#            if len(color_searching) == 0:
#                coloring_grph
                
#                else:
                    
#        for i in range(len(node_stack)):
#            coloring_node = node_stack.pop()
#            for j in range(len(adjset)):
#                for j in range(len(adjset):
 #                   if
    def assign_colors():
        def replace_operand(op):
            if type(op) == tuple:
                if op[0] == REG:
#                    print (op)
                    return (REG, color_map[op[1]])
#                    return (REG, 0)
                elif op[0] == MEM:
                    return (MEM, replace_operand(op[1]), op[2])
                else:
                    return op
            else:
                return op
        def replace_instruction(inst):
            r=[]
            r.append(inst[0])
            for op in inst[1:]:
                r.append(replace_operand(op))
            return tuple(r)
        for i in range(len(ir)):
            ir[i]= replace_instruction(ir[i])
    liveness_analysis()
    liveness_print()
    build_interference_graph()
    simplify_and_select()
    assign_colors()

def irs_gen(irs, outfile):
    with open(outfile, 'w') as out:
        print("""
.text
.globl main
.type main, @function
""", file=out)
        for ir in irs:
            for i in ir:
                if i[0] in [LABEL, PROLOGUE]:
                    print("%s" % ir_inst2gas(i), file=out)
                else:
                    print("      %s" % ir_inst2gas(i), file=out)
            print("", file=out)

def main():
    ofname='gcd.s'
    irs=INPUT_IRS
    for ir in irs:
        ir_reg_alloc(ir)
    irs_print_in_gas(irs)
    irs_gen(irs, ofname)
    r=subprocess.call(['/class/ec3204_2013/x86/bin/gcc', '-o', 'gcd', ofname], shell=False)
    assert r == 0
    r=subprocess.call(['./gcd'], shell=False)
    assert r == 1
    print("Congrualation on your success!")

if __name__ == "__main__":
    main()

