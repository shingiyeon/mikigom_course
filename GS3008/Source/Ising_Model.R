Ann = function(A, m, n, nr, nc) {
  if (m == nr) Ann1 = A[1,n] else Ann1 = A[m+1,n] # bottom
  if (n == 1) Ann2 = A[m,nc] else Ann2 = A[m,n-1] # left
  if (m == 1) Ann3 = A[nr,n] else Ann3 = A[m-1,n] # top
  if (n == nc) Ann4 = A[m,1] else Ann4 = A[m,n+1] # right
  return(Ann1 + Ann2 + Ann3 + Ann4)
}

flip_or_not = function(A, x, y, de, Tem){
  if(de<0)
    return (TRUE)
  else if(runif(1, min=0, max=1)<exp(-de/Tem))
    return (TRUE)
  else
    return (FALSE)
}

Ising_model_2D <- function(nr, nc) {
  E=0
  Esq=0
  Esq_avg=0
  E_avg=0
  etot=0
  etotsq=0
  M=0
  Msq=0
  Msq_avg=0
  M_avg=0
  mtot=0
  mtotsq=0
  Mabs=0
  Mabs_avg=0
  Mq_avg=0
  mabstot=0
  mqtot=0
  de=0
  
  A = matrix(nrow = nr, ncol = nc)
  R = matrix(nrow = nscans, ncol = 5, byrow=TRUE, dimnames=list(rep("",nscans),c("T","E_av","Cv","Mag_av","Mag_sus")))

  for(i in seq(1, nr))
    for(j in seq(1, nc))
      A[i, j] = 1
  
  for (isc in 1:nscans) { # T scan loop
    temp = T_hi - dT*(isc - 1)
    
    x=0
    y=0
    de=0
    
    for(a in seq(1, transient))
    {
      for(b in seq(1,n))
      {
        x = sample(nr,1,replace=TRUE)
        y = sample(nc,1,replace=TRUE)
        de = -2*Ann(A, x, y, nr, nc)
        
        if(flip_or_not(A, x, y, de))
        {
          A[x, y] = -A[x, y]
        }
      }
    }
    
    M=total_magnetization()
    Mabs=abs(total_magnetization())
    E=total_energy()

    etot=0
    etotsq=0
    mtot=0
    mtotsq=0
    mabstot=0
    mqtot=0
    
    for (a in seq(1, mcs))
    {
      for (b in seq(1,n))
      {
        x = runif(1, min = 1, max = size+1)
        y = runif(1, min = 1, max = size+1)
        de = -2*Ann(A, x, y, nr, nc)
        
        if(flip_or_not(A, x, y, de, Tem))
        {
          A[x, y] = - A[x,y]
          
          E = E + 2*de
          M = M + 2*A[x, y]
          Mabs = Mabs + abs(A[x,y])
        }
      }

      etot = etot + E/2.0
      etotsq = etotsq + E/2.0*E/2.0
      mtot = motot + M
      mtotsq = mtotsq + M*M
      mqtot = mqtot + M*M*M*M
      mabstot = mabstot + sqrt(M*M)
    } # T scan 종료
  
    E_avg=etot*norm
    Esq_avg=etotsq*norm
    M_avg=mtot*norm
    Msq_avg=mtotsq*norm
    Mabs_avg=mabstot*norm
    Mq_avg=mqtot*norm
    
  R
  return (R)
}

nr = 8; nc = 8;
M8 <- Ising_model_2D(nr, nc)

nr = 10; nc = 10;
M10 <- Ising_model_2D(nr, nc)

nr = 12; nc = 12;
M12 <- Ising_model_2D(nr, nc)

plot(M8[,1], M8[,2], xlab = "T", ylab = "<E>/N", main="<E>/N", ylim=c(-0.6, -2.0), pch=4, type="o", col="#228B22")
#par(new=T)
#plot(M10[,1], M10[,2], ylab="", xlab="", ylim=c(-0.6, -2.0), pch=0, type="o", col="#FF3030")
#par(new=T)
#plot(M12[,1], M12[,2], ylab="", xlab="", ylim=c(-0.6, -2.0), pch=2, type="o", col="#009ACD")
#legend(x=2.7,	y=-1.6, c("L=12", "L=10","L=8"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF3030","#228B22"))

dev.new()
plot(M8[,1], M8[,4], xlab = "T", ylab = "<|M|>/N", main="Spontaneous Magnetization vs. Temperature", ylim = c(0,1.0), pch=4, type="o", col="#228B22")
#par(new=T)
#plot(M10[,1], M10[,4], ylab="", xlab="", ylim = c(0,1.0), pch=0, type="o", col="#FF3030")
#par(new=T)
#plot(M12[,1], M12[,4], ylab="", xlab="", ylim = c(0,1.0), pch=2, type="o", col="#009ACD")
#legend(x=2.7,y=0.8, c("L=12", "L=10","L=8"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF3030","#228B22"))

dev.new()
plot(M8[,1], M8[,3], xlab = "T", ylab = "Cv/N", main="Heat Capacity vs. Temperature", ylim=c(0,0.016), pch=4, type="o", col="#228B22")
#par(new=T)
#lot(M10[,1], M10[,3], ylab="", xlab="", ylim=c(0,0.02), pch=0, type="o", col="#FF3030")
#par(new=T)
#lot(M12[,1], M12[,3], ylab="", xlab="", ylim=c(0,0.02), pch=2, type="o", col="#009ACD")
#legend(x=2.7,y=0.015, c("L=12", "L=10","L=8"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF3030","#228B22"))
#abline(v=2.3,col="red",lty="dotted")

dev.new()
plot(M8[,1], M8[,5], xlab = "T", ylab = "X/N", main="Magnetic Susceptibility vs. Temperature", ylim=c(0,0.20), pch=4, type="o", col="#228B22")
#par(new=T)
#plot(M10[,1], M10[,5], ylab="", xlab="", ylim=c(0,0.20), pch=0, type="o", col="#FF3030")
#par(new=T)
#plot(M12[,1], M12[,5], ylab="", xlab="", ylim=c(0,0.20), pch=2, type="o", col="#009ACD")
#legend(x=1.7,y=0.05, c("L=12", "L=10","L=8"), cex=0.7, pch=c(2,0,4),col=c("#009ACD","#FF3030","#228B22"))
#abline(v=2.3,col="red",lty="dotted")