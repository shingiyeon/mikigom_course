particular_integration_function <- function(X){
	n = 10000000
	theta_random = runif(n, min=0, max=pi)
	r_random = runif(n, min=0, max=1)
	sum = 0

	for(i in seq(1, 10000000)){
		sum = sum + 2*pi*(1/(1+((X-r_random[i]*cos(theta_random[i]))^2+(r_random[i]*sin(theta_random[i]))^2)/(1-r_random[i]^2))^(1/2))/n
	}

	print(sum)
}