import subprocess
from time import sleep
import end_existence

p = subprocess.Popen(['/bin/bash', '-i', '-c', 'awakenmychild'])
sleep(5)

end_existence.main()

p.terminate()
#end_existence.main()