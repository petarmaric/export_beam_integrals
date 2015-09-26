from beam_integrals.beam_types import BaseBeamType 
from beam_integrals.integrals import BaseIntegral, integrate

from ..app import app


@app.task
def compute_integral(integral_id, beam_type_id, m, t, v, n):
    beam_type = BaseBeamType.coerce(beam_type_id)
    integral = BaseIntegral.coerce(integral_id)
    max_mode = app.conf.BEAM_INTEGRALS_MAX_MODE
    decimal_precision = app.conf.BEAM_INTEGRALS_DECIMAL_PRECISION

    result, error = integrate(
        integral, beam_type,
        a=1.,
        m=m, t=t, v=v, n=n,
        decimal_precision=decimal_precision,
        error=True
    )

    cache_key = integral.cache_key(m, t, v, n, max_mode=max_mode)
    data = {
        'integral_float64': float(result),
        'error_float64': float(error),
        'integral_str': str(result),
        'error_str': str(error),
    }
    return cache_key, data

@app.task
def combine_computed_integrals_into_a_table(computed_integrals, integral_id):
    return integral_id, dict(computed_integrals)
