MC_integration <- function(x0, delta_x, N)
{
	x = x0

	exponential_vector = seq(1, floor(log10(N)))
	probability_vector = rep(1, floor(log10(N)))

	for(i in seq(1,floor(log10(N)))){exponential_vector[i] = 10^(i-1)}

	for(i in seq(1,floor(log10(N)))){
		N_vector<-c(1:exponential_vector[i])
		sum = x0*x0

		for(j in N_vector){
			x_old=x
			random_walking = runif(1, min=0, max=1)
		
			if(random_walking <= 0.5){x = x + delta_x}
			else{x = x - delta_x}
	
			delta_E = x*x - x_old*x_old

			if(delta_E <= 0){sum = sum + x*x}
			else{
				random_r = runif(1, min=0, max=1)

				if(exp(-delta_E)>random_r){sum = sum + x*x}
				else{
					sum = sum + x_old*x_old
					x = x_old
				}
			}
		}
		probability_vector[i] = (sum)/(exponential_vector[i])
}

print("Probability :")
print(probability_vector)
error = abs(probability_vector-1/2)
print("Coefficient of linear regression :")
print(cor(log10(exponential_vector), log10(error)))
e_vector = log10(error)
n_vector = log10(exponential_vector)
result<-lm(e_vector~n_vector)
print("Summary :")
print(summary(result))
plot(log10(exponential_vector), log10(error), abline(lm(log10(error)~log10(exponential_vector))), xlab = "log(N)", ylab = "log(error)", main="Metropolis-Hastings integration")
}