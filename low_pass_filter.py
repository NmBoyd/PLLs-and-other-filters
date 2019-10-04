import scipy.signal

def lpf1(x,alpha):
    '''1-pole low-pass filter with coefficient alpha = 1/tau'''
    return scipy.signal.lfilter([alpha], [1, alpha-1], x)
def rms(e):
    '''root-mean square'''
    return np.sqrt(np.mean(e*e))
def maxabs(e):
    '''max absolute value'''
    return max(np.abs(e))

alphas = [0.2,0.1,0.05,0.02]
estimates = [lpf1(pos_measured, alpha) for alpha in alphas]


fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(2,1,1)
ax.plot(t,pos_exact,'k')
for y in estimates:
    ax.plot(t,y)
ax.set_ylabel('position')
ax.legend(['exact'] + ['$\\alpha = %.2f$' % alpha for alpha in alphas])

ax = fig.add_subplot(2,1,2)
for alpha,y in zip(alphas,estimates):
    err = y-pos_exact
    ax.plot(t,err)
    ax.set_ylabel('position error')
    print 'alpha=%.2f -> rms error = %.5f, peak error = %.4f' % (alpha, rms(err), maxabs(err))