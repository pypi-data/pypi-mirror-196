class Fraction:

  # parameterized constructor
  def __init__(self,x,y,a,b):
    self.num1 = x
    self.den1 = y
    self.num2 = a
    self.den2 = b

  def Fra_add(self):
    new_num = self.num1 * self.den2 + self.num2 * self.den1
    new_den = self.den1 * self.den2
    return f"{new_num}/{new_den}"

  def Fra_sub(self):
    new_num = self.num1 * self.den2 - self.num2 * self.den1
    new_den = self.den1 * self.den2
    return f"{new_num}/{new_den}"

  def Fra_mul(self):
    new_num = self.num1 * self.num2
    new_den = self.den1 * self.den2
    return f"{new_num}/{new_den}"

  def Fra_div(self):
    new_num = self.num1 * self.den2
    new_den = self.den1 * self.num2
    return f"{new_num}/{new_den}"

  def Fra_lt_gt(self):
    new_num = self.num1 * self.den2
    new_den = self.num2 * self.den1
    if new_num > new_den:
      return f"{self.num1}/{self.den1} is greater than {self.num2}/{self.den2}"
    elif new_num < new_den:
      return f"{self.num2}/{self.den2} is greater than {self.num1}/{self.den1}"
    else:
      return f"{self.num1}/{self.den1} is equal to {self.num2}/{self.den2}"