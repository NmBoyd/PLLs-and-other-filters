# PLLs-and-other-filters
Phase-locked loops (PLLs) — given oscillating inputs, a variable-frequency oscillator attempts to follow those inputs by using a phase detector and a feedback loop to try to drive the phase error to zero.

Tracking loops — an estimator attempts to follow the input by using an error and a feedback loop to try to drive the error to zero. (Similar to a PLL, but without the oscillating part.)

Luenberger observers — a type of tracking loop that tries to simulate the dynamics of the real system, and adds a corrective term based on a fixed gain applied to the difference between real and simulated systems.

Adaptive filters (e.g. Least Mean Square or Recursive Least Squares filters) — a type of tracking loop that tries to simulate the dynamics of the real system, then uses the error between real and simulated system to adjust the parameters of the simulation

Kalman filters — essentially a Luenberger observer with a variable gain, where the variable gain is derived from estimates of measurement noise to determine the optimal gain.