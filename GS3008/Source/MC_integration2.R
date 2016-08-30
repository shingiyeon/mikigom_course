MC_integration2 <- function(x_0, delta_x, N)
{
	N_vector <-c(1:N)
	probability_vector <- rep(1, N)
	sum = x_0*x_0
	
	for(i in N_vector){
		random_walking = runif(1, min=0, max=1)
		
		if(random_walking <= 0.5){x_new = x_0 + delta_x}
		else{x_new = x_0 - delta_x}

		delta_E = x_new*x_new - x_0*x_0

		if(delta_E <= 0){sum = sum + x_new*x_new}
		else{
			random_r = runif(1, min=0, max=1)

			if(exp(-delta_E)>random_r){sum = sum + x_new*x_new}
			else{
				sum = sum + x_0*x_0
			}
		}
		probability_vector[i] = (sum-x_0*x_0)/(i)
	}
print(probability_vector[N])
error = abs(probability_vector-1/2)
plot(log10(N_vector), log10(error), xlab = "log(N)", ylab = "log(error)", main="MC_integration")
}