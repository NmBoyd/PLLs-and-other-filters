import numpy as np
import matplotlib.pyplot as plt

# Phase Locked Loop (PLLS)

t = np.linspace(0,5,10000)
def simpll(tlist,A,B,omega0,phi0):
    def helper():
        phi = phi0
        x = -omega0
        omega = -x - B*np.sin(phi)
        it = iter(tlist)
        tprev = it.next()
        yield(tprev, omega, phi, x)
        for t in it:
            dt = t - tprev
            # Verlet solver:
            phi_mid = phi + omega*dt/2
            x += A*np.sin(phi_mid)*dt
            omega = -x - B*np.sin(phi_mid)
            phi = phi_mid + omega*dt/2
            tprev = t
            yield(tprev, omega, phi, x)
    return np.array([v for v in helper()])

v = simpll(t,A=1800,B=10,omega0=140,phi0=0)
omega = v[:,1]
phi = v[:,2]

fig = plt.figure(figsize=(8,6), dpi=80)
ax = fig.add_subplot(2,1,1)
ax.plot(t,omega)
ax.set_ylabel('$\\tilde{\\omega}$',fontsize=20)
ax = fig.add_subplot(2,1,2)
ax.plot(t,phi/(2*np.pi))
ax.set_ylabel('$\\tilde{\\phi}/2\\pi$ ',fontsize=20)
ax.set_xlabel('t',fontsize=16)

# ---------------------------------------------- #

# fig = plt.figure(figsize=(8,6), dpi=80)
# ax = fig.add_subplot(1,1,1)
# ax.plot(phi/(2*np.pi),omega)
# ax.set_xlabel('phase error (cycles) = $\\tilde{\\phi}/2\\pi$', fontsize=16)
# ax.set_ylabel('velocity error (rad/sec) = $\\tilde{\\omega}$', fontsize=16)
# ax.grid('on')

# ---------------------------------------------- #

# fig = plt.figure(figsize=(8,6), dpi=80)
# ax = fig.add_subplot(1,1,1)

# t = np.linspace(0,5,2000)
# for i in xrange(-2,2):
#     for s in [-2,-1,1,2]:
#         omega0 = s*100
#         v = simpll(t,A=1800,B=10,omega0=omega0,phi0=(i/2.0)*np.pi)
#         omega = v[:,1]
#         phi = v[:,2]
#         k = math.floor(phi[-1]/(2*np.pi) + 0.5)
#         phi -= k*2*np.pi
#         for cycrepeat in np.array([-2,-1,0,1,2])+np.sign(s):
#             ax.plot(phi/(2*np.pi)+cycrepeat,omega,'k')
# ax.set_ylim(-120,120)
# ax.set_xlim(-1.5,1.5)
# ax.set_xlabel('$\\tilde{\\phi}/2\\pi$ ',fontsize=20)
# ax.set_ylabel('$\\tilde{\\omega}$ ',fontsize=20)

# ---------------------------------------------- #
# SCALAR VS VECTOR PLLS

# t = np.linspace(0,1,1000)
# tpts = np.linspace(0,1,5)
# f = lambda t: 0.9*cos(2*np.pi*t)
# ''' f(t)  = A*cos(omega*t)'''
# fderiv = lambda t: -0.9*2*np.pi*sin(2*np.pi*t)
# ''' f'(t) = -A*omega*sin(omega*t)'''
# fig = plt.figure(figsize=(8,6),dpi=80); ax=fig.add_subplot(1,1,1)
# ax.plot(t,f(t))
# phasediff = 6.0/360
# plt.plot(t,f(t+phasediff),'gray')
# plt.plot(tpts,f(tpts),'b.',markersize=7)
# h=plt.plot(tpts,f(tpts+phasediff),'.',color='gray',markersize=7)
# for t in tpts:
#     slope = fderiv(t)
#     a = 0.1
#     ax.plot([t-a,t+a],[f(t)-slope*a,f(t)+slope*a],'r-')
# ax.grid('on')
# ax.set_xlim(0,1)
# ax.set_xticks(np.linspace(0,1,13))
# ax.set_xticklabels(['%d' % x for x in np.linspace(0,360,13)]);

# ---------------------------------------------- #
# Two sine waves 90 degree apart

# t = np.linspace(0,1,1000)
# f = lambda A,t: np.vstack([0.9*np.cos(t*2*np.pi),
#                          0.9*np.sin(t*2*np.pi)]).transpose()
# plt.plot(t*360,f(0.9,t))
# plt.plot(t*360,f(0.9,t+6.0/360),'gray')
# plt.xlim(0,360)
# plt.xticks(np.linspace(0,360,13))

# atan2(y,x) method

# def phase_estimate_2d(A,n,N=20000):
#     t = np.linspace(0,1,N)
#     xy_nonoise = f(A,t)
#     xy = xy_nonoise + n * np.random.randn(N,2)
#     x = xy[:,0]; y = xy[:,1]
#     plt.plot(x,y,'.')
#     plt.plot(xy_nonoise[:,0],xy_nonoise[:,1],'-r')
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.figure()
#     def principal_angle(x,c=1.0):
#         ''' find the principal angle: between -c/2 and +c/2 '''
#         return (x+c/2)%c - c/2
#     phase_error_radians = principal_angle(np.arctan2(y,x) - t*2*np.pi, 2*np.pi)
#     plt.plot(t,phase_error_radians)
#     plt.ylabel('phase error, radians')
#     print 'n/A = %.4f' % (n/A)
#     print 'rms phase error = ',rms(phase_error_radians)
# phase_estimate_2d(0.9,0.02)

# Unwrapping function

# angles = np.array([90,117,136,160,-171,-166,-141,-118,-83,-42,-27,3,68,-152,-20,17,63])
# ierror=13
# angles2 = angles+0.0; angles2[ierror] = 44
# unwrap_deg = lambda deg: np.unwrap(deg/180.0*np.pi)*180/np.pi
# fig=plt.figure()
# ax=fig.add_subplot(1,1,1)
# msz=4
# ax.plot(angles,'+r',markersize=msz)
# ax.plot(unwrap_deg(angles),'+-b',markersize=msz)
# ax.plot(angles2,'xr',markersize=msz)
# ax.plot(ierror,angles[ierror],'+g',markersize=msz)
# ax.plot(ierror,angles2[ierror],'xg',markersize=msz)
# ax.plot(unwrap_deg(angles2),'x:b',markersize=msz)
# ax.legend(('principal angle','unwrapped angle'),'best')
# ax.set_yticks(np.arange(-180,900,90));