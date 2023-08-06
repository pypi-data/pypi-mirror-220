from hak.one.dict.cell.make import f as make_cell
from hak.one.dict.rate.to_str_frac import f as to_str_frac
from hak.pxyz import f as pxyz
from hak.one.string.print_and_return_false import f as pf
from hak.one.string.colour.bright.green import f as g
from hak.one.string.colour.bright.red import f as r

# make_row
def f(widths, record, names):
  return "| "+ ' | '.join([
    (
      make_cell({
        'value': record[n] if n in record else None,
        'width': widths[n],
        'format': to_str_frac if n.startswith('rate_') else None
      })
    ) for n in names
  ])+ " |"


def t_a():
  x_widths = {'a': 1, 'b': 1}
  x_r =      {'a': 0, 'b': 1}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|   | 1 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_b():
  x_widths = {'a': 1, 'b': 1}
  x_r =      {'a': 2, 'b': 3}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 2 | 3 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_c():
  x_widths = {'a': 1, 'b': 1, 'c': 1}
  x_r =      {'a': 0, 'b': 1, 'c': 2}
  x_names =  ['a', 'b', 'c']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|   | 1 | 2 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_d():
  x_widths = {'a': 1, 'b': 1, 'c': 1}
  x_r =      {'a': 2, 'b': 3}
  x_names =  ['a', 'b', 'c']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 2 | 3 |   |'
  z = f(**x)
  return pxyz(x, y, z)

def t_e():
  x_widths = {'a': 1, 'b': 1, 'c': 1}
  x_r =      {'a': 0, 'b': 1}
  x_names =  ['a', 'b', 'c']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|   | 1 |   |'
  z = f(**x)
  return pxyz(x, y, z)

def t_f():
  x_widths = {'a': 1, 'b': 1, 'c': 1}
  x_r =      {'a': 2, 'b': 3, 'c': 4}
  x_names =  ['a', 'b', 'c']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 2 | 3 | 4 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_g():
  x_widths = {'aa': 2, 'b': 1}
  x_r =      {'aa': 0, 'b': 1}
  x_names =  ['aa', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|    | 1 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_h():
  x_widths = {'aa': 2, 'b': 1}
  x_r =      {'aa': 2, 'b': 3}
  x_names =  ['aa', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|  2 | 3 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_i():
  x_widths = {'a': 2, 'b': 2}
  x_r =      {'a': 10, 'b': 11}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 10 | 11 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_j():
  x_widths = {'a': 2, 'b': 2}
  x_r =      {'a': 12, 'b': 13}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 12 | 13 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_k():
  x_widths = {'a': 2, 'b': 2}
  x_r =      {'a': 10, 'b': 1}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 10 |  1 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_l():
  x_widths = {'a': 2, 'b': 2}
  x_r =      {'a': 2, 'b': 13}
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|  2 | 13 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_m():
  x_widths = {'c': 2, 'b': 2, 'a': 2}
  x_r =      {'a': 10, 'b': 1}
  x_names =  ['c', 'b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|    |  1 | 10 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_n():
  x_widths = {'c': 2, 'b': 2, 'a': 2}
  x_r =      {'a': 2, 'b': 13}
  x_names =  ['c', 'b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|    | 13 |  2 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_o():
  x_widths = {'c': 2, 'b': 2, 'a': 2}
  x_r =      {'a': 3, 'b': 12, 'c': 15}
  x_names =  ['c', 'b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 15 | 12 |  3 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_p():
  x_widths = {'c': 2, 'a': 2}
  x_r =      {'a': 10}
  x_names =  ['c', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|    | 10 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_q():
  x_widths = {'c': 2, 'a': 2}
  x_r =      {'a': 2}
  x_names =  ['c', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|    |  2 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_r():
  x_widths = {'c': 2, 'a': 2}
  x_r =      {'a': 3, 'c': 15}
  x_names =  ['c', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 15 |  3 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_s():
  x_widths = {'b': 2, 'a': 2}
  x_r =      {'a': 10, 'b': 1}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|  1 | 10 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_t():
  x_widths = {'b': 2, 'a': 2}
  x_r =      {'a': 2, 'b': 13}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 13 |  2 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_u():
  x_widths = {'b': 2, 'a': 2}
  x_r =      {'a': 3, 'b': 12, 'c': 15}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 12 |  3 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_v():
  x_widths = {'b': 2, 'a': 1}
  x_r =      {'a': True, 'b': 1}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"|  1 | {g('Y')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_w():
  x_widths = {'b': 2, 'a': 1}
  x_r =      {'a': False, 'b': 13}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"| 13 | {r('N')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_x():
  x_widths = {'b': 2, 'a': 1}
  x_r =      {'a': False, 'b': 12, 'c': 15}
  x_names =  ['b', 'a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"| 12 | {r('N')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_y():
  x_widths = {'b': 2, 'is_revenue': 7}
  x_r =      {'is_revenue': True, 'b': 1}
  x_names =  ['b', 'is_revenue']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"|  1 |       {g('Y')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_z():
  x_widths = {'b': 2, 'is_revenue': 7}
  x_r =      {'is_revenue': False, 'b': 13}
  x_names =  ['b', 'is_revenue']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"| 13 |       {r('N')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_aa():
  x_widths = {'b': 2, 'is_revenue': 7}
  x_r =      {'is_revenue': False, 'b': 12, 'c': 15}
  x_names =  ['b', 'is_revenue']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = f"| 12 |       {r('N')} |"
  z = f(**x)
  return pxyz(x, y, z)

def t_ab():
  x_widths = {'b': 2, 'balance_a': 7}
  x_r =      {'balance_a': 1.0, 'b': 13}
  x_names =  ['b', 'balance_a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 13 |    1.00 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ac():
  x_widths = {'b': 2, 'balance_a': 7}
  x_r =      {'balance_a': 1.1, 'b': 12, 'c': 15}
  x_names =  ['b', 'balance_a']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 12 |    1.10 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ad():
  x_widths = {
    'description': 30,
    'flow_AUD': 8,
    'flag_asset_aud_cash': 5,
    'flag_equity_retained_earnings': 8
  }
  x_r =      {'description': 'Opening transaction'}
  x_names =  [
    'description',
    'flow_AUD',
    'flag_asset_aud_cash',
    'flag_equity_retained_earnings'
  ]
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|            Opening transaction |          |       |          |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ae():
  x_widths = {
    'description': 30,
    'flow_AUD': 8,
    'flag_asset_aud_cash': 5,
    'flag_equity_retained_earnings': 8
  }
  x_r =      {
    'description': 'Deposit 1000 AUD',
    'flow_AUD': 1000.0,
    'flag_asset_aud_cash': 1,
    'flag_equity_retained_earnings': 1
  }
  x_names =  [
    'description',
    'flow_AUD',
    'flag_asset_aud_cash',
    'flag_equity_retained_earnings'
  ]
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|               Deposit 1000 AUD |  1000.00 |     1 |        1 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_af():
  x_widths = {
    'description': 30,
    'flow_AUD': 8,
    'flag_asset_aud_cash': 5,
    'flag_equity_retained_earnings': 8
  }
  x_r =      {
    'description': 'Exchanged 1000 AUD for 100 USD',
    'flow_AUD': -1000.0,
    'flow_USD': 100.0,
    'flag_asset_aud_cash': -1,
    'flag_asset_usd_cash_as_aud': 1
  }
  x_names =  [
    'description',
    'flow_AUD',
    'flag_asset_aud_cash',
    'flag_equity_retained_earnings'
  ]
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| Exchanged 1000 AUD for 100 USD | -1000.00 |    -1 |          |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ag():
  x_widths = {'a': 4, 'b': 4}
  x_r =      {
    'a': {'numerator': 0, 'denominator': 1, 'unit': {'m': 1}},
    'b': {'numerator': 1, 'denominator': 1, 'unit': {'$': 1}}
  }
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|      | 1.00 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ah():
  x_widths = {'a': 4, 'b': 4}
  x_r =      {
    'a': {'numerator': 2, 'denominator': 1, 'unit': {'m': 1}},
    'b': {'numerator': 3, 'denominator': 1, 'unit': {'$': 1}}
  }
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 2.00 | 3.00 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_ai():
  x_widths = {'a': 4, 'b': 4}
  x_r =      {
    'a': {'numerator': 0, 'denominator': 1, 'unit': {}},
    'b': {'numerator': 1, 'denominator': 2, 'unit': {'$': 1, 'm': -1}}
  }
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '|      | 0.50 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_aj():
  x_widths = {'a': 4, 'b': 4}
  x_r =      {
    'a': {'numerator': 2, 'denominator': 1, 'unit': {}},
    'b': {'numerator': 3, 'denominator': 2, 'unit': {'$': 1, 'm': -1}}
  }
  x_names =  ['a', 'b']
  x = {'widths': x_widths, 'record': x_r, 'names': x_names}
  y = '| 2.00 | 1.50 |'
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  if not t_c(): return pf('!t_c')
  if not t_d(): return pf('!t_d')
  if not t_e(): return pf('!t_e')
  if not t_f(): return pf('!t_f')
  if not t_g(): return pf('!t_g')
  if not t_h(): return pf('!t_h')
  if not t_i(): return pf('!t_i')
  if not t_j(): return pf('!t_j')
  if not t_k(): return pf('!t_k')
  if not t_l(): return pf('!t_l')
  if not t_m(): return pf('!t_m')
  if not t_n(): return pf('!t_n')
  if not t_o(): return pf('!t_o')
  if not t_p(): return pf('!t_p')
  if not t_q(): return pf('!t_q')
  if not t_r(): return pf('!t_r')
  if not t_s(): return pf('!t_s')
  if not t_t(): return pf('!t_t')
  if not t_u(): return pf('!t_u')
  if not t_v(): return pf('!t_v')
  if not t_w(): return pf('!t_w')
  if not t_x(): return pf('!t_x')
  if not t_y(): return pf('!t_y')
  if not t_z(): return pf('!t_z')
  if not t_aa(): return pf('!t_aa')
  if not t_ab(): return pf('!t_ab')
  if not t_ac(): return pf('!t_ac')
  if not t_ad(): return pf('!t_ad')
  if not t_ae(): return pf('!t_ae')
  if not t_af(): return pf('!t_af')
  if not t_ag(): return pf('!t_ag')
  if not t_ah(): return pf('!t_ah')
  if not t_ai(): return pf('!t_ai')
  if not t_aj(): return pf('!t_aj')
  return True
