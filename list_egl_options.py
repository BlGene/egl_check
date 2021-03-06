import os
import subprocess

if not os.path.isfile('./EGL_options.o'):
    subprocess.call(['bash', './build.sh'])

print("----------Default-------------")
p = subprocess.Popen(['./EGL_options.o'], stderr=subprocess.PIPE)
p.wait()
out, err = p.communicate()
print(err)

N = err.decode("utf-8").split(" of ")[1]
N = int(N[0])
print("number of EGL devices: {}".format(N))

for i in range(N):
    print("----------Option #{} (id={})-------------".format(i+1,i))
    my_env = os.environ.copy()
    my_env["EGL_VISIBLE_DEVICE"] = "{}".format(i)
    p = subprocess.Popen(['./EGL_options.o'], env=my_env)
    p.wait()
    print()

