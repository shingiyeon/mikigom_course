Ann = function(A, m, n) {
  if (m == nr) Ann1 = A[1,n] else Ann1 = A[m+1,n] # bottom
  if (n == 1) Ann2 = A[m,nc] else Ann2 = A[m,n-1] # left
  if (m == 1) Ann3 = A[nr,n] else Ann3 = A[m-1,n] # top
  if (n == nc) Ann4 = A[m,1] else Ann4 = A[m,n+1] # right
  return(Ann1 + Ann2 + Ann3 + Ann4)
}

nr = 8; nc = 8 # Number of rows and columns
A = matrix(nrow = nr, ncol = nc)
npass = 2e5 # Number of passes for each temperature
nequil = 1e5 # Number of equilibration steps for each T
T_hi = 3 # Temperature to start scan at
T_lo = 1.5 # Temperature to finish scan at
dT = 0.1 # Temperature scanning interval
nscans = as.integer((T_hi - T_lo)/dT) + 1
# Initialize results table
M8 = matrix(nrow = nscans, ncol = 5, byrow=TRUE, dimnames=list(rep("",nscans),c("T","E_av","Cv","Mag_av","Mag_sus")))

T_energy_sample = seq(1, nequil)
T_magnetization_sample = seq(1, nequil)

for (sIc in 1:nscans) { # T scan loop
  temp = T_hi - dT*(sIc - 1)
  # Initialize variables
  beta = 1/temp
  oc = 0 # output count
  E_av = 0
  E2_av = 0
  mag_av = 0
  mag2_av = 0
  
  A[1,1] = 1
  for (i in 1:(nr - 1)) A[i+1,1] = -A[i,1]
  for (j in 1:(nc - 1)) A[,j+1] = -A[,j]
  
  for (ipass in 0:npass) { # Monte Carlo passes at T
    if (ipass > nequil) {
      oc = oc + 1 # output count
      mag = sum(A)/(nr*nc)
      mag_av = mag_av + mag
      mag2_av = mag2_av + mag^2
      E = 0
      for (m in 1:nr) {
        for (n in 1:nc) {
          E = E - A[m,n]*Ann(A,m,n)
        }
      }
      E = E/(2*nr*nc)
      E_av = E_av + E
      E2_av = E2_av + E^2
      if (temp == 2.0 && ipass != 0){
        T_energy_sample[ipass-nequil] = E_av/(ipass-nequil)
        T_magnetization_sample[ipass-nequil] = mag_av/(ipass-nequil)
      }
    }
    # Choose a random spin to change  
    m = sample(nr,1,replace=TRUE)
    n = sample(nc,1,replace=TRUE)
    ts = -A[m,n] # Flip sign of spin
    dU = -2*ts*Ann(A,m,n)
    eta = runif(1)
    if(exp(-beta*dU) > eta) A[m,n] = ts
  } # end MC passes at T
  
  M8[sIc,1] = temp
  M8[sIc,2] = E_av/oc
  M8[sIc,3] = beta^2*(E2_av/oc - (E_av/oc)^2)
  M8[sIc,4] = abs(mag_av/oc)
  M8[sIc,5] = beta*(mag2_av/oc - (mag_av/oc)^2)
  cat(c(temp, mag_av,mag2_av,E_av,E2_av),"\n") # not shown
  if (temp == 2.0){
    plot(seq(1, nequil), T_energy_sample, xlab = "N", ylab = "Total energy (E/N)", main = "Total Energy Configuration @ Tem=2.0 & L=8", type = 'l', col="#228B22")
    dev.new()
    plot(seq(1, nequil), T_magnetization_sample, xlab = "N", ylab = "Total magnetization (M/N)", main = "Total magnetization @ Tem=2.0 & L=8", type = 'l', col="#228B22")
    dev.new()
  }
} # end T scans

nr = 10; nc = 10 # Number of rows and columns
A = matrix(nrow = nr, ncol = nc)
npass = 2e5 # Number of passes for each temperature
nequil = 1e5 # Number of equilibration steps for each T
T_hi = 3 # Temperature to start scan at
T_lo = 1.5 # Temperature to finish scan at
dT = 0.1 # Temperature scanning interval
nscans = as.integer((T_hi - T_lo)/dT) + 1
# Initialize results table
M10 = matrix(nrow = nscans, ncol = 5, byrow=TRUE, dimnames=list(rep("",nscans),c("T","E_av","Cv","Mag_av","Mag_sus")))

for (sIc in 1:nscans) { # T scan loop
  temp = T_hi - dT*(sIc - 1)
  # Initialize variables
  beta = 1/temp
  oc = 0 # output count
  E_av = 0
  E2_av = 0
  mag_av = 0
  mag2_av = 0
  # Set up initial checkerboard spin configuration
  A[1,1] = 1
  for (i in 1:(nr - 1)) A[i+1,1] = -A[i,1]
  for (j in 1:(nc - 1)) A[,j+1] = -A[,j]
  for (ipass in 0:npass) { # Monte Carlo passes at T
    if (ipass > nequil) {
      oc = oc + 1 # output count
      mag = sum(A)/(nr*nc)
      mag_av = mag_av + mag
      mag2_av = mag2_av + mag^2
      E = 0
      for (m in 1:nr) {
        for (n in 1:nc) {
          E = E - A[m,n]*Ann(A,m,n)
        }
      }
      E = E/(2*nr*nc)
      E_av = E_av + E
      E2_av = E2_av + E^2
    }
    # Choose a random spin to change  
    m = sample(nr,1,replace=TRUE)
    n = sample(nc,1,replace=TRUE)
    ts = -A[m,n] # Flip sign of spin
    dU = -2*ts*Ann(A,m,n)
    log_eta = log(runif(1))
    if(-beta*dU > log_eta) A[m,n] = ts
  } # end MC passes at T
  M10[sIc,1] = temp
  M10[sIc,2] = E_av/oc
  M10[sIc,3] = beta^2*(E2_av/oc - (E_av/oc)^2)
  M10[sIc,4] = abs(mag_av/oc)
  M10[sIc,5] = beta*(mag2_av/oc - (mag_av/oc)^2)
  cat(c(temp, mag_av,mag2_av,E_av,E2_av),"\n") # not shown
} # end T scans

nr = 12; nc = 12 # Number of rows and columns
A = matrix(nrow = nr, ncol = nc)
npass = 2e5 # Number of passes for each temperature
nequil = 1e5 # Number of equilibration steps for each T
T_hi = 3 # Temperature to start scan at
T_lo = 1.5 # Temperature to finish scan at
dT = 0.1 # Temperature scanning interval
nscans = as.integer((T_hi - T_lo)/dT) + 1
# Initialize results table
M12 = matrix(nrow = nscans, ncol = 5, byrow=TRUE, dimnames=list(rep("",nscans),c("T","E_av","Cv","Mag_av","Mag_sus")))

for (sIc in 1:nscans) { # T scan loop
  temp = T_hi - dT*(sIc - 1)
  # Initialize variables
  beta = 1/temp
  oc = 0 # output count
  E_av = 0
  E2_av = 0
  mag_av = 0
  mag2_av = 0
  # Set up initial checkerboard spin configuration
  A[1,1] = 1
  for (i in 1:(nr - 1)) A[i+1,1] = -A[i,1]
  for (j in 1:(nc - 1)) A[,j+1] = -A[,j]
  for (ipass in 0:npass) { # Monte Carlo passes at T
    if (ipass > nequil) {
      oc = oc + 1 # output count
      mag = sum(A)/(nr*nc)
      mag_av = mag_av + mag
      mag2_av = mag2_av + mag^2
      E = 0
      for (m in 1:nr) {
        for (n in 1:nc) {
          E = E - A[m,n]*Ann(A,m,n)
        }
      }
      E = E/(2*nr*nc)
      E_av = E_av + E
      E2_av = E2_av + E^2
    }
    # Choose a random spin to change  
    m = sample(nr,1,replace=TRUE)
    n = sample(nc,1,replace=TRUE)
    ts = -A[m,n] # Flip sign of spin
    slc = nscans - sIc
    dU = -2*ts*Ann(A,m,n)
    log_eta = log(runif(1))
    if(-beta*dU > log_eta) A[m,n] = ts
  } # end MC passes at T
  M12[sIc,1] = temp
  M12[slc,2] = E_av/oc
  M12[sIc,3] = beta^2*(E2_av/oc - (E_av/oc)^2)
  M12[sIc,4] = abs(mag_av/oc)
  M12[sIc,5] = beta*(mag2_av/oc - (mag_av/oc)^2)
  cat(c(temp, mag_av,mag2_av,E_av,E2_av),"\n") # not shown
} # end T scans

plot(M8[,1], M8[,2], xlab = "T", ylab = "<E>/N", main="<E>/N vs. Tem @ L = 8", type = 'o')

dev.new()
plot(M8[,1], M8[,4], xlab = "T", ylab = "<|M|>/N", main="<|M|>/N vs. Tem @ L = 8", type = 'o')

dev.new()
plot(M8[,1], M8[,3], xlab = "T", ylab = "Cv/N", main="Cv/N vs. Tem", ylim=c(0,0.03), pch=4, type="o")
par(new=T)
plot(M10[,1], M10[,3], ylab="", xlab="", ylim=c(0,0.03), pch=0, type="o")
par(new=T)
plot(M12[,1], M12[,3], ylab="", xlab="", ylim=c(0,0.03), pch=2, type="o")
legend(x=2.7,y=0.015, c("L=8", "L=10","L=12"), cex=0.7, pch=c(2,0,4))
abline(v=2.3,col="red",lty="dotted")

dev.new()
plot(M8[,1], M8[,5], xlab = "T", ylab = "X/N", main="Magnetic Susceptibility vs. Tem", ylim=c(0,0.40), pch=4, type="o")
par(new=T)
plot(M10[,1], M10[,5], ylab="", xlab="", ylim=c(0,0.40), pch=0, type="o")
par(new=T)
plot(M12[,1], M12[,5], ylab="", xlab="", ylim=c(0,0.40), pch=2, type="o")
legend(x=1.7,y=0.05, c("L=8", "L=10","L=12"), cex=0.7, pch=c(2,0,4))
abline(v=2.3,col="red",lty="dotted")