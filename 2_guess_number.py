# 猜数小游戏
# 游戏者给出猜数范围，如1-100
# 程序猜测这个数字，游戏者给出反馈
__author__ = 'huhu, <huyoo353@126.com>'
def find_middle(start, end):
  #print start, end
  return round((start+end)/2.0)
if __name__ == '__main__':
  start, end = '',''
  text = input("> 输入猜数的范围（如：421-499 或者421 499 或者421,499）:")
  spliters = '-, '
  for c in spliters:
    if text.find(c) != -1:
      num_list = text.split(c)
      if ''.join(num_list).isdigit():
        start, end = num_list[0],num_list[1]
        break
  if start == '' or end == '':
    print ("范围不正确")
  else:
    start = int(start)
    end  = int(end)
    count = 1
    last_guess = find_middle(start,end)
    while 1:
      result = input(u"放弃猜测直接回车, 等于输入=, 小了输入1, 大了请输入2\n>>> #猜数[%d] ,对吗？> " % last_guess )
      #print type(text)
      if result in ['q','e','exit','quit','bye',u'退出']:
        print ('Bye!')
        break
      else:
        result=result.strip()
        if result == '1':
          start = last_guess
          last_guess = find_middle(last_guess,end)
        elif result == '2':
          end = last_guess
          last_guess = find_middle(start,last_guess)
        elif result == '=':
          print ('恭喜猜中, 共猜了%d次' % count)
          print ('#猜数[%d]' % last_guess)
          break
        else: #
          continue
        count += 1