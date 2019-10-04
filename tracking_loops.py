import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------- #

t = np.linspace(0,4,5000)
pos_exact = (np.abs(t-0.5) - np.abs(t-1.5) - np.abs(t-2.5) + np.abs(t-3.5))/2
pos_measured = pos_exact + 0.04*np.random.randn(t.size)

fig = plt.figure(figsize=(8,6),dpi=80)
ax = fig.add_subplot(1,1,1)
ax.plot(t,pos_measured,'.',markersize=2)
ax.plot(t,pos_exact,'k')
ax.set_ylim(-0.5,1.5)

# ---------------------------------------------- #

# def trkloop(x,dt,kp,ki):
#     def helper():
#         velest = 0
#         posest = 0
#         velintegrator = 0
#         for xmeas in x:
#             posest += velest*dt
#             poserr = xmeas - posest
#             velintegrator += poserr * ki * dt
#             velest = poserr * kp + velintegrator
#             yield (posest, velest, velintegrator)
#     y = np.array([yi for yi in helper()])
#     return y[:,0],y[:,1],y[:,2]

# [posest,velest,velestfilt] = trkloop(pos_measured,t[1]-t[0],kp=40.0,ki=900.0)

# fig = plt.figure(figsize=(8,6),dpi=80)
# ax = fig.add_subplot(2,1,1)
# ax.plot(t,pos_exact,'k',t,posest)
# ax.set_ylabel('position')

# ax = fig.add_subplot(2,1,2)
# err = posest-pos_exact
# ax.plot(t,posest-pos_exact)
# ax.set_ylabel('position error')
# print 'rms error = %.5f, peak error = %.4f' % (rms(err), maxabs(err))

# fig = plt.figure(figsize=(8,6),dpi=80)
# ax = fig.add_subplot(1,1,1)
# vel_exact = (t > 0.5) * (t < 1.5) + (-1.0*(t > 2.5) * (t < 3.5))
# ax.plot(t,velest,'y',t,velestfilt,'b',t,vel_exact,'r')