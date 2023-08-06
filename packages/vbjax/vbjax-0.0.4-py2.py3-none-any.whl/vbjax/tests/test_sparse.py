import numpy as np
import jax
import jax.numpy as jnp
import scipy.sparse

def test_csr_scipy():
    n = 10
    A: scipy.sparse.csr_matrix = scipy.sparse.random(n, n, density=0.1).tocsr()
    nx = np.random.randn(n)
    jx = jnp.array(nx)
    def matvec(x):
        return A @ x
    b = matvec(jx)
    print(b)


if __name__ == '__main__':
    test_csr_scipy()
