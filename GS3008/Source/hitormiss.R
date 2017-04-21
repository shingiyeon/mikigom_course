hitormiss <- function(k){
n=0
m=0
error=rep(1,k)

for (i in 1:k){
    randomnum <- runif(2, min=-1, max=1)
    if (randomnum[1]*randomnum[1]+randomnum[2]*randomnum[2]<1){n=n+1}
    m=m+1
    error[i] = abs(pi-4*n/m)
}
plot(log10(seq(1:k)), log10(error), xlab = "log(N)", ylab = "log(error)", main="Hit or Miss", type = 'l')
}