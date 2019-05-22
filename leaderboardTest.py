tFile = open("leaderboard.txt",'r+')



names = []
scores = []

list = tFile.read().splitlines()
iterator = True
i=int(0)
ender = len(list)-1
while iterator:
	name,score = list.pop(0).split(":")
	names.append(name)
	scores.append(int(score))
	i = i+1
	#print(i)
	if i>ender:
		iterator = False
	else:
		x = 1
print(scores)

# n = len(scores)

# # for i in range(n):
 
# #         # Last i elements are already in place
# #         for j in range(0, n-i-1):
 
# #             # traverse the array from 0 to n-i-1
# #             # Swap if the element found is greater
# #             # than the next element
# #             if scores[j] < scores[i] :
# #                 scores[j], scores[i] = scores[i], scores[j]
# #                 names[j],names[i]=names[i],names[j]
# # flag = False
# # i=0
# # while !flag:
# # 	if 

# #scores.sort()
# # for index in range(0,n-1):

# # 	currentvalue = scores[index]
# # 	nameC = names[index]
# # 	position = 0
# # 	print(position)

# # 	while position>=0 and scores[position]>=currentvalue:
# # 		scores[position]=scores[position+1]
# # 		print(scores)
# # 		position = position+1


# # 	scores[position]=currentvalue
# # 	names[position] = nameC

# index = 0

# while index < len(scores):
# 	temp = scores[index]
# 	test =  index -1 
# 	resetflag = False
# 	while (test>=0) and (resetflag == False):
# 		if temp < list[test]:
# 			scores[test+1] = scores[test]
# 			test = test - 1
# 			if test == -1:
# 				resetflag = True
# 		else:
# 			resetflag = True
# 	scores[test+1] = temp
# 	index+=1
# 	#print(list)
# print(scores)



# print("\n"+str(names))
# print(scores)
# print(119>30)
# print(n)







# # listy = [1,2,3,4,6,5]

# # length = len(listy)

# # for i in range(0,length-1,1):
# # 	for n in range(0,)






def insertionSort(alist):
   for index in range(1,len(alist)):

     currentvalue = alist[index]
     position = index

     while position>0 and alist[position-1]>currentvalue:
         alist[position]=alist[position-1]
         position = position-1

     alist[position]=currentvalue

alist = []
insertionSort(scores)
print(scores)


