import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
# ---------------------------------------------- #

# Create a trapezoidal position signal with additive gaussian white noise

t = np.linspace(0,4,5000)
pos_exact = (np.abs(t-0.5) - np.abs(t-1.5) - np.abs(t-2.5) + np.abs(t-3.5))/2
pos_measured = pos_exact + 0.04*np.random.randn(t.size)

fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(1,1,1)
ax.plot(t,pos_measured,'.',markersize=2)
ax.plot(t,pos_exact,'k')
ax.set_ylim(-0.5,1.5)
plt.title('Trapezoidal Signal Profile with White Noise')

plt.show()

# ---------------------------------------------- #

def trkloop(x,dt,kp,ki):
    def helper():
        velest = 0
        posest = 0
        velintegrator = 0
        for xmeas in x:
            posest += velest*dt
            poserr = xmeas - posest
            velintegrator += poserr * ki * dt
            velest = poserr * kp + velintegrator
            yield (posest, velest, velintegrator)
    y = np.array([yi for yi in helper()])
    return y[:,0],y[:,1],y[:,2]

def lpf1(x,alpha):
    '''1-pole low-pass filter with coefficient alpha = 1/tau'''
    return scipy.signal.lfilter([alpha], [1, alpha-1], x)
def rms(e):
    '''root-mean square'''
    return np.sqrt(np.mean(e*e))
def maxabs(e):
    '''max absolute value'''
    return max(np.abs(e))

# Apply a Low pass Filter to reduce the white noise
## Low pass filter doesn't do very well tracking ramp waveforms: the time delay causes a DC offset

alphas = [0.2,0.1,0.05,0.02]
estimates = [lpf1(pos_measured, alpha) for alpha in alphas]

fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(2,1,1)
ax.plot(t,pos_exact,'k')
for y in estimates:
    ax.plot(t,y)
ax.set_ylabel('position')
ax.legend(['exact'] + ['$\\alpha = %.2f$' % alpha for alpha in alphas])
plt.title('Low Pass Filter Results')

ax = fig.add_subplot(2,1,2)
for alpha,y in zip(alphas,estimates):
    err = y-pos_exact
    ax.plot(t,err)
    ax.set_ylabel('position error')
    plt.title('Low Pass Filter Error')
    print ("alpha=%.2f -> rms error = %.5f, peak error = %.4f" % (alpha, rms(err), maxabs(err)))
print ("Low Pass Filters don't provide velocity estimate")
# Create a tracking loop to reduce the white noise
## model the system and drive the steady-state error to zero

[posest,velest,velestfilt] = trkloop(pos_measured,t[1]-t[0],kp=40.0,ki=900.0)

fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(2,1,1)
ax.plot(t,pos_exact,'k',t,posest)
ax.set_ylabel('position')
plt.title('Tracking Loop Filter Results')

ax = fig.add_subplot(2,1,2)
err = posest-pos_exact
ax.plot(t,posest-pos_exact)
ax.set_ylabel('position error')
plt.title('Tracking Loop Filter Error')
print("rms error = %.5f, peak error = %.4f" % (rms(err), maxabs(err)))

fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(1,1,1)
vel_exact = (t > 0.5) * (t < 1.5) + (-1.0*(t > 2.5) * (t < 3.5))
ax.plot(t,velest,'y',label='Estimated Velocity')
ax.plot(t,velestfilt,'b',label='Filtered Estimate Velocity')
ax.plot(t,vel_exact,'r',label='Exact Velocity')
ax.legend()
plt.title('Tracking Loop Estimated Velocity')
print ("Tracking Loops can estimate velocity")


plt.show()