size44 <<- 4
size88 <<- 8
size1616 <<- 16
lattice44 <- matrix(nrow = size44, ncol = size44)
lattice88 <- matrix(nrow = size88, ncol = size88)
lattice1616 <- matrix(nrow = size1616, ncol = size1616)
n44 <<- size44*size44
n88 <<- size88*size88
n1616 <<- size1616*size1616
T_min <<- 0.5
T_delta <<- 0.1
mcs_num <<- 10000
transient <<- 1000
norm44 <<- 1/(mcs_num*n44)
norm88 <<- 1/(mcs_num*n88)
norm1616 <<- 1/(mcs_num*n1616)

for(i in seq(1, size44)){
  for(j in seq(1, size44)){
    lattice44[i, j] = 1
  }
}

for(i in seq(1, size88)){
  for(j in seq(1, size88)){
    lattice88[i, j] = 1
  }
}

for(i in seq(1, size1616)){
  for(j in seq(1, size1616)){
    lattice1616[i, j] = 1
  }
}

Ising_Model <- function() {
  
  temperature = seq(1,46)
  energy_configuration44 = seq(1,46)
  magnetic_configuration44 = seq(1,46)
  heat_capacity44 = seq(1, 46)
  susceptibility44 = seq(1, 46)
  binder44 = seq(1, 46)
  energy_configuration88 = seq(1,46)
  magnetic_configuration88 = seq(1,46)
  heat_capacity88 = seq(1, 46)
  susceptibility88 = seq(1, 46)
  binder88 = seq(1, 46)
  energy_configuration1616 = seq(1,46)
  magnetic_configuration1616 = seq(1,46)
  heat_capacity1616 = seq(1, 46)
  susceptibility1616 = seq(1, 46)
  binder1616 = seq(1, 46)
  
  T3_energy_sample = seq(1, mcs_num)
  T3_magnetization_sample = seq(1, mcs_num)
  
  iteration = 0
  for(Tem in rev(seq(T_min, 5.0, T_delta))){
    
    print (Tem)
    iteration = iteration + 1
    
    transient_result(Tem, size44)
    transient_result(Tem, size88)
    transient_result(Tem, size1616)
    
    M44 = total_magnetization(size44)
    Mabs44 = abs(total_magnetization(size44))
    E44 = total_energy(size44)
    M88 = total_magnetization(size88)
    Mabs88 = abs(total_magnetization(size88))
    E88 = total_energy(size88)
    M1616 = total_magnetization(size1616)
    Mabs1616 = abs(total_magnetization(size1616))
    E1616 = total_energy(size1616)
    
    etot44=0
    etotsq44=0
    mtot44=0
    mtotsq44=0
    mabstot44=0
    mqtot44=0
    etot88=0
    etotsq88=0
    mtot88=0
    mtotsq88=0
    mabstot88=0
    mqtot88=0
    etot1616=0
    etotsq1616=0
    mtot1616=0
    mtotsq1616=0
    mabstot1616=0
    mqtot1616=0
    
    se =0
    
    for(i in seq(1, mcs_num)){
      for(j in seq(1, n44)){
        x = floor(runif(1, min=1, max=size44+1))
        y = floor(runif(1, min=1, max=size44+1))
        if(step_test(x, y, se, Tem, size44)){
          flip(x, y, size44)
          E44 = E44 + 2*se
          M44 = M44 + 2*lattice44[x, y]
          Mabs44 = Mabs44 + abs(lattice44[x, y])
        }
      }
      etot44 = etot44 + E44/2
      etotsq44 = etotsq44 + (E44/2)*(E44/2)
      mtot44 = mtot44 + M44
      mtotsq44 = mtotsq44 + M44*M44
      mqtot44 = mqtot44 + M44*M44*M44*M44
      mabstot44 = mabstot44 + abs(M44)
      
      if(Tem == 3.0){
        T3_energy_sample[i] = etot44/(i*n44)
        T3_magnetization_sample[i] = mtot44/(i*n44)
      }
    }
    
    for(i in seq(1, mcs_num)){
      for(j in seq(1, n88)){
        x = floor(runif(1, min=1, max=size88+1))
        y = floor(runif(1, min=1, max=size88+1))
        if(step_test(x, y, se, Tem, size88)){
          flip(x, y, size88)
          E88 = E88 + 2*se
          M88 = M88 + 2*lattice88[x, y]
          Mabs88 = Mabs88 + abs(lattice88[x, y])
        }
      }
      etot88 = etot88 + E88/2
      etotsq88 = etotsq88 + (E88/2)*(E88/2)
      mtot88 = mtot88 + M88
      mtotsq88 = mtotsq88 + M88*M88
      mqtot88 = mqtot88 + M88*M88*M88*M88
      mabstot88 = mabstot88 + abs(M88)
    }
    
    for(i in seq(1, mcs_num)){
      for(j in seq(1, n1616)){
        x = floor(runif(1, min=1, max=size1616+1))
        y = floor(runif(1, min=1, max=size1616+1))
        if(step_test(x, y, se, Tem, size1616)){
          flip(x, y, size1616)
          E1616 = E1616 + 2*se
          M1616 = M1616 + 2*lattice1616[x, y]
          Mabs1616 = Mabs1616 + abs(lattice1616[x, y])
        }
      }
      etot1616 = etot1616 + E1616/2
      etotsq1616 = etotsq1616 + (E1616/2)*(E1616/2)
      mtot1616 = mtot1616 + M1616
      mtotsq1616 = mtotsq1616 + M1616*M1616
      mqtot1616 = mqtot1616 + M1616*M1616*M1616*M1616
      mabstot1616 = mabstot1616 + abs(M1616)
    }
    
    E_avg44 = etot44*norm44
    Esq_avg44 = etotsq44*norm44
    M_avg44 = mtot44*norm44
    Msq_avg44 = mtotsq44*norm44
    Mabs_avg44 = mabstot44*norm44
    Mq_avg44 = mqtot44*norm44
    E_avg88 = etot88*norm88
    Esq_avg88 = etotsq88*norm88
    M_avg88 = mtot88*norm88
    Msq_avg88 = mtotsq88*norm88
    Mabs_avg88 = mabstot88*norm88
    Mq_avg88 = mqtot88*norm88
    E_avg1616 = etot1616*norm1616
    Esq_avg1616 = etotsq1616*norm1616
    M_avg1616 = mtot1616*norm1616
    Msq_avg1616 = mtotsq1616*norm1616
    Mabs_avg1616 = mabstot1616*norm1616
    Mq_avg1616 = mqtot1616*norm1616
    
    temperature[iteration] = Tem
    energy_configuration44[iteration] = E_avg44
    magnetic_configuration44[iteration] = M_avg44
    heat_capacity44[iteration] = (Esq_avg44-(E_avg44*E_avg44*size44))/(Tem*Tem)
    susceptibility44[iteration] = (Msq_avg44-(M_avg44*M_avg44*size44))/Tem
    binder44[iteration] = 1 - ((Mq_avg44)/(3*Msq_avg44))
    energy_configuration88[iteration] = E_avg88
    magnetic_configuration88[iteration] = M_avg88
    heat_capacity88[iteration] = (Esq_avg88-(E_avg88*E_avg88*size88))/(Tem*Tem)
    susceptibility88[iteration] = (Msq_avg88-(M_avg88*M_avg88*size88)/Tem)
    binder88[iteration] = 1 - ((Mq_avg88)/(3*Msq_avg88))
    energy_configuration1616[iteration] = E_avg1616
    magnetic_configuration1616[iteration] = M_avg1616
    heat_capacity1616[iteration] = (Esq_avg1616-(E_avg1616*E_avg1616*size1616))/(Tem*Tem)
    susceptibility1616[iteration] = (Msq_avg1616-(M_avg1616*M_avg1616*size1616))/Tem
    binder1616[iteration] = 1 - ((Mq_avg1616)/(3*Msq_avg1616))
                                   
    if(Tem == 3.0){
       plot(seq(1, mcs_num), T3_energy_sample, xlab = "Monte Carlo Iteration Number", ylab = "Total energy (E/N)", main = "Total Energy Configuration @ L=4 & Tem=3.0", type = 'l', col="#228B22")
       dev.new()
       plot(seq(1, mcs_num), T3_magnetization_sample, xlab = "Monte Carlo Iteration Number", ylab = "Total magnetization (M/N)", main = "Total magnetization @ L=4 & Tem = 3.0", type = 'l', col="#228B22")
     }
                                   
  }
  dev.new()
  plot(temperature, energy_configuration44, xlab = "Temperature", ylab = "Energy per spin (E/N)", main="Energy vs. Temperature @ L=4", pch=4, type="o", col="#228B22")
  
  dev.new()
  plot(temperature, magnetic_configuration44, xlab = "Temperature", ylab = "Spontaneous Magnetization per spin (<|M|>/N)", ylim=c(0,1), main="Spontaneous Magnetization vs. Temperature @ L=4", pch=4, type="o", col="#228B22")
  
  dev.new()
  plot(temperature, heat_capacity44, xlab = "Temperature", ylab = "Heat Capacity per spin (C/N)", main="Heat Capacity vs. Temperature", pch=4, type="o", col="#228B22")
  par(new=T)
  plot(temperature, heat_capacity88, ylab="", xlab="", pch=0, type="o", col="#FF1616")
  par(new=T)
  plot(temperature, heat_capacity1616, ylab="", xlab="", pch=2, type="o", col="#009ACD")
  #	legend(x=,y=, c("L=30", "L=20","L=10"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF1616","#228B22"))
  
  dev.new()
  plot(temperature, susceptibility44, xlab = "Temperature", ylab = "Susceptibility per spin (X/N)", ylim=c(0,8), main="Susceptibility vs. Temperature", pch=4, type="o", col="#228B22")
  par(new=T)
  plot(temperature, susceptibility88, ylab="", xlab="", ylim=c(0,8), pch=0, type="o", col="#FF1616")
  par(new=T)
  plot(temperature, susceptibility1616, ylab="", xlab="", ylim=c(0,8), pch=2, type="o", col="#009ACD")
  #	legend(x=4,y=6, c("L=12", "L=8","L=4"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF1616","#228B22"))
  
  dev.new()
  plot(temperature, binder44, xlab = "Temperature", ylab = "Binder Cumulant", ylim=c(0,8), main="Binder Cumulant vs. Temperature", pch=4, type="o", col="#228B22")
  par(new=T)
  plot(temperature, binder88, ylab="", xlab="", ylim=c(0,8), pch=0, type="o", col="#FF1616")
  par(new=T)
  plot(temperature, binder1616, ylab="", xlab="", ylim=c(0,8), pch=2, type="o", col="#009ACD")
  #	legend(x=4,y=6, c("L=12", "L=8","L=4"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF1616","#228B22"))
  
  
}

position_energy <- function(x, y, size){
  if(x==size) {r <- 1}
  else {r <- x+1}
  if(x==1) {l <- size}
  else {l <- x-1}
  if(y==size) {u <- 1}
  else {u <- y+1}
  if(y==1) {d <- size}
  else {d <- y-1}
  
  if (size == size44) {return (-1*lattice44[x,y]*(lattice44[l,y]+lattice44[r,y]+lattice44[x,u]+lattice44[x,d]))}
  else if (size == size88) {return (-1*lattice88[x,y]*(lattice88[l,y]+lattice88[r,y]+lattice88[x,u]+lattice88[x,d]))}
  else {return (-1*lattice1616[x,y]*(lattice1616[l,y]+lattice1616[r,y]+lattice1616[x,u]+lattice1616[x,d]))}
}

step_test <- function(x, y, de, Tem, size){
  eval.parent(substitute(de <- -2*position_energy(x, y, size)))
  if (de < 0) {return(TRUE)}
  else if(runif(1, min=0, max=1)<exp(-de/Tem)) {return(TRUE)}
  else {return(FALSE)}
}

flip <- function(x, y, size){
  if (size == size44) {eval.parent(substitute(lattice44[x,y] <- -1 * lattice44[x,y]))}
  else if (size == size88) {eval.parent(substitute(lattice88[x,y] <- -1 * lattice88[x,y]))}
  else {eval.parent(substitute(lattice1616[x,y] <- -1 * lattice1616[x,y]))}
}

transient_result <- function(Tem, size){
  se=0
  for(i in seq(1,transient)){
    for(j in seq(1,size*size)){
      x = floor(runif(1, min=1, max=(size + 1)))
      y = floor(runif(1, min=1, max=(size + 1)))
      if(step_test(x, y, se, Tem, size)) {flip(x, y, size)}
    }
  }
}

total_energy <- function(size){
  E=0
  for(i in rev(seq(1, size))){
    for(j in seq(1, size)){
      E <- E + position_energy(i, j, size)
    }
  }
  return (E)
}

total_magnetization <- function(size){
  M = 0
  for(i in rev(seq(1, size))){
    for(j in seq(1, size)){
      if(size == size44) {M <- M + lattice44[i, j]}
      else if(size == size88) {M <- M + lattice88[i, j]}
      else {M <- M + lattice1616[i, j]}
    }
  }
  return (M)
}