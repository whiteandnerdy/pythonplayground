
#!C:\Users\jniswonger\AppData\Local\Programs\Python\Python35-32\python

text = "This is a sentence"
lengthOfText = len(text)

print("the sentence: \' "+text+"\' has as length of: ", lengthOfText)


for i in range(3,11):
	print(i)
	
	
def fib(n):
	a,b =0,1
	while a < n:
		print(a, end=' ')
		a,b = b,a+b
		print()
		
		
		
fib(35)