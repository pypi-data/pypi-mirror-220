# %%
import hmq


# %%
@hmq.task()
def divide(a, b):
    return a / b


divide(4, 3)
divide(1, 2)
divide(1, 1)
tag = divide.submit(
    tag="tagme",
    ncores=2,
    datacenters="Kassel,Toronto",
    packages="numpy,scipy".split(","),
)


@hmq.task()
def mul(a, b):
    return a * b


mul(4, 3)
mul(1, 2)
mul(1, 1)
tag = mul.submit(
    tag="tagme2",
    packages="numpy,scipy".split(","),
)
# py-3.10,nc-2,dc-Kassel
# py-3.10,nc-2,dc-any
tag.pull()
# # %%


# mols = (1,2,3)
# for i in mols:
#     divide(mols, 1)

# #%%
# for i in mols:
#     divide(mols, 1)

# #%%


# %%
@hmq.task
def sleep(n):
    import time

    time.sleep(1)
    return n


for i in range(10000):
    sleep(2)
tag = sleep.submit(tag="tagme")
# %%
# get results
tag.pull()
# %%
tag.pull()
# %%
tag.to_file("test.hmq")
# %%
tag = hmq.Tag.from_file("test.hmq")
# %%
tag.pull()
# %%
