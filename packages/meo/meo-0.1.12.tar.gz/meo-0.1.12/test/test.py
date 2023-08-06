import sys
import os

sys.path.insert(0, os.path.curdir)

from meo.crack import Crack
import meo

# pdf = Crack.pdf("./examples/data/cannot_edit.pdf")
# pdf.remove_pdf_password("./output.pdf")
# pdf = Crack.pdf("./examples/data/cannot_open.pdf")
# pdf.remove_pdf_password("./output.pdf")
wait = Crack.zip("./test/flag.zip")
res = wait.in_multiprocess_by_seed(meo.crack.utils.PWD_SEED_COMPLEX, progressbar=0, gc_interval=100)
print(res)