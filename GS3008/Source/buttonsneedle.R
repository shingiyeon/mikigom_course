buffon.needle <- function(d, l, n, m){
	touch = 0
	probability = 0
	random_postion=0
	random_theta=0
	theta_vector = rep(1,n)
	probability_vector = rep(1,n)

	for (i in 1:n){
		touch = 0
		random_theta <- runif(1, min=0, max=pi)

		for (k in 1:m){
			random_position <- runif(1, min=0, max=d/2)
			if(random_position+(l/2)*sin(random_theta)>(d/2)) {touch=touch+1}
			}

		probability = touch / m
		theta_vector[i] = random_theta
		probability_vector[i] = probability
		}

plot(theta_vector,probability_vector, xlab = "Theta", ylab = "Probability", main="Boffun's needle")	
}