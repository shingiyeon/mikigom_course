# The parameters X is given as the function works. The output of function is a value of f(X, 0). n is set as 1000000.

particular_integration_function <- function(X){
	n=100000
	theta_random = runif(n, min=0, max=pi)
	r_random = runif(n, min=0, max=1)
	sum = 0

	for(i in seq(1, n)){
		r = r_random[i]
		theta = theta_random[i]
		sum = sum + 2*pi*(1/(1+((X-r*cos(theta))^2+(r*sin(theta))^2)/(1-r^2))^(1/2))/n
	}
	print(sum)
}