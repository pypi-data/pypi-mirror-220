pythonQdata ={
1:
'''
Write a Python program to create all possible strings by using'a', 'e', 'i', 'o', 'u

''',
2:
'''
Write a Python program to create all possible permutations from a given collection of distinct numbers.
''',
3:
'''
Write a Python program to check the priority of the four operators (+, -, *, /).
''',
4:
'''
Write a Python program that accepts a sequence of lines (blank line to terminate) as input and #prints the lines as output (allcharacters in lower case).

''',
5:
'''
Write a Python program to check the validity of password input by users.
''',
6:
'''
Write a program to print the Floyd’s triangle.
''',
7:
'''
 Write a program to read month of year as an integer. Then display the name of the month.
''',
8:
'''
Write a program that accepts any number and prints the number of digits in thenumber.
''',
9:
'''
 Write a Python function to check whether a number is in a given range.
''',
10:
'''
Write a Python function that prints out the first n rows of Pascal's triangle.
''',
11:
'''
Write a Python recursive program to calculate the sum of thepositive integers of n+(n- 2)+(n-4)... (until n-x =< 0).
''',
12:
'''
Write a Python recursive program to calculate the harmonic sumof n-1
''',
13:
'''
Write a Python recursive program to find the greatest commondivisor (gcd) of two integers
''',
14:
'''
Write a program that uses the lambda function to multiply twonumbers.
''',
15:
'''
 Write a program that passes a lambda function as an argument toanother program to compute the cube of a number.
''',
16:
'''
Write a program to compute lambda (n) for all positive values of n where,lambda(n) can be recursively defined as lambda(n)=lamda(n/2) +1 if n>1
''',
17:
'''
Write a Python program to find the list of words that are longer than n from a given list of words.
''',
18:
'''
Write a Python program to create a list by concatenating a given list whose range goes from 1 to n
''',
19:
'''
Write a Python program to find missing and additional values in two lists
''',
20:
'''
Write a program to insert a value in a list at the specified location.
''',
21:
'''
Write a program to find the sum of all values in a list using reduce () function.
''',
22:
'''
Write a Python program to remove an empty tuple(s) from a list of tuples.
''',
23:
'''
Write a Python program to unzip a list of tuples into individual lists
''',
24:
'''
write a program that creates a list ['a','b','c'] ,then creates a tuple from that list.Now do the opposite.That is ,create the tuple ('a','b','c'), and then create a list from it.
''',
25:
'''
Write a program to make two sets of random integers and apply all set operations on them.
''',
26:
'''
Write a Python program to sort a given dictionary by key.
''',
27:
'''
Write a Python program to create and display all combinations of letters, selecting each letter from a different key in a dictionary.
''',
28:
'''
Write a Python program to create a dictionary from two lists without losing duplicate values.
''',
29:
'''
Python Program to find the number of occurences ofeach letter in a string
''',
30:
'''
Write A Program that Reads a text file and counts the number of occurrences of a givenword.
''',
31:
'''
 Write a program to compare two files.
''',
32:
'''
 Write programs that exchange the contents of two files.
''',
33:
'''
write a program to count the number of records stored in the file employee
''',
34:
'''
Write a program to merge two files into a third file. The names of the files must beentered using command line arguments.
''',
35:
'''
 Write a function program to read the data from a file and count the total number of linesand words in the file.
''',


}
pythonAdata ={
1:
'''
def toString(List): 
    return ''.join(List)
def permute(a, l, r):
    if l ==r:
        print(toString(a))
    else:
        for i in range(l, r):
            a[l], a[i] = a[i], a[l]
            permute(a, l+1, r)
            a[l], a[i] = a[i], a[l]

string ="aeiou"
n = len(string)
a =list(string)
permute(a, 0, n)
''',
2:
'''
from itertools import permutations

l=eval(input("Enter list:"))
myList = list(permutations(l))
print("Permutations\\n",myList)
''',
3:
'''
a=int(input("Enter a Value:"))
b=int(input("Enter b Value:"))
c=int(input("Enter c Value:"))
result=a+b-c
print("Result of (a+b-c)",result)
result=a-b+c
print("Result of (a-b+c)",result)
result=a+b*c
print("Result of (a+b*c)",result)
result=a-b/c
print("Result of (a-b/c)",result)
result=a*b/c
print("Result of (a*b/c)",result)
result=a/b*c
print("Result of (a/b*c)",result)

''',
4:
'''
lines = []
while True:
    l = input()
    if l:
        lines.append(l.lower())
    else:
        break
    for l in lines:
        print(l)
''',
5:
'''
import re
def validate_password(password):
    if len(password) < 6 or len(password ) > 16 :return
    False
    if not re.search("[a-z]", password):return
    False
    if not re.search("[A-Z]", password):return
    False
    if not re.search("[0-9]", password):return
    False
    if not re.search("[$#@]",password):return
    False
    return True
password =input("Enter password to validity : ")
if validate_password(password):
    print("Valid password")
else:
    print("Invalid password")
''',
6:
'''
rows = int(input("Please Enter the total Number of Rows : "))
number = 1
print("Floyd's Triangle")
for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(number,end = ' ')
        number = number + 1
    print()
''',
7:
'''
month=int(input("Enter a month of the year"))
if month==1:
    print("January")
elif month==2:
    print("February")
elif month==3:
    print("March")
elif month==4:
    print("April")
elif month==5:
    print("May")
elif month==6:
    print("June")
elif month==7:
    print("July")
elif month==8:
    print("August")
elif month==9:
    print("September")
elif month==10:
    print("October")
elif month==11:
    print("November")
elif month==12:
    print("December")
else:
    print("Enter a month from 1 to 12")
''',
8:
'''
n=int(input("Enter number:"))
count=0
while(n>0):
    count=count+1
    n=n//10
print("The number of digits in the number are:",count)
''',
9:
'''
def within_range(number, start, end):
    if start <= number <= end:
        print(number,"is present between" ,start,"and ",end)
    else:
        print("Number is not within the range")
n=int(input('Enter the number:'))
r1,r2=[int (i) for i in input("Enter the range values(r1r2):").split()]
within_range(n,r1,r2)
''',
10:
'''
def pascal_triangle(n):
    row = [1]
    for i in range(n):
        print(' '.join(str(x) for x in row))
        row = [1] + [row[j] + row[j+1] for j in range(len(row)-1)] + [1]


r=int(input('Enter no of rows:'))
pascal_triangle(r)
''',
11:
'''
def Sum_of_integers(n):
    if n<0:
        return 0
    else:
        return n+Sum_of_integers(n-2)
n=int(input('Enter n value:'))
print("Sum of integers is:",Sum_of_integers(n))
''',
12:
'''
def harmonic_sum(n):
    if n<2:
        return 1
    else:
        return 1/n+harmonic_sum(n-1)
n=int(input("Enter n Value:"))
print("Harmonic Sum is",harmonic_sum(n))
''',
13:
'''
def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)
a=int(input("Enter first number:"))
b=int(input("Enter second number:"))
output =gcd(a,b)
print("Greatest Common Divisor is: ",output)
''',
14:
'''
f=lambda x,y:x*y
x=int(input("Enter xvalue:"))
y=int(input("Enter y value:"))
mul=f(x,y)
print("Multiplication is",mul)
''',
15:
'''
cube = lambda x: x**3
def find_cube(func, num):
    return func(num)
n=int(input("Enter a number:"))
result = find_cube(cube, n)
print(result)
''',
16:
'''
n=int(input("Enter n :"))
res= lambda n : 0 if n < 1 else 1+ res(n//2)
print(res(n))

''',
17:
'''
str=input("Enter any string:")
l=str.split(' ')
n=int(input("Enter n:"))
l1=[]
for i in l:
    if len(i) > n:
        l1.append(i)
print("List of words that are longer than n :",l1)
''',
18:
'''
my_list = ['p', 'q']
n = 4
new_list = ['{}{}'.format(x, y) for y in range(1, n+1) for x in my_list ]
print(new_list)
''',
19:
'''
list1 = ['a','b','c','d','e','f']
list2 = ['d','e','f','g','h']
print('Missing values in second list: ', ','.join(set(list1).difference(list2)))
print('Additional values in second list: ', ','.join(set(list2).difference(list1)))
''',
20:
'''
l=[12,43,65,87,10]
print("Original list is :",l)
i=int(input("Enter index to insert a value:"))
val=int(input("Enter the value to be inserted at specified location:"))
l.insert(i,val)
print("After insert a value in a list at the specified location is:",l)
''',
21:
'''
from functools import reduce
l=eval(input("Enter list of elements:"))
sum=reduce(lambda x,y:x+y,l)
print("Sum of all values in list is ",sum)
''',
22:
'''
L = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
print("Original list : ",L)
L = [t for t in L if t]
print("After removal of empty tuples from a list of tuples, list is:",L)
''',
23:
'''
list1=[1,2,3,4,5,6]
list2=['a','b','c','d','e']
list3=list(zip(list1,list2))
print("List elements after zipping",list3)
print("List elements after Unzipping",list(zip(*list3)))
''',
24:
'''
l=['a','b','c']
t=tuple(l) #converts list to tuple
print(t)
l1=list(t) #converts tuple to list
print(l1)

''',
25:
'''
set1={1,55,66,23,78,65,99,95}
set2={1,66,23,78,95,65,99,55,24,26}
print("Set 1:", set1)
print("Set 2:", set2)
union = set1.union(set2)
intersection = set1.intersection(set2)
difference = set1.difference(set2)
symmetric_difference = set1.symmetric_difference(set2)
subset_check = set1.issubset(set2)
print("Union:", union)
print("Intersection:", intersection)
print("Difference (Set 1 - Set 2):", difference)
print("Difference (Set 2 - Set 1):", set2.difference(set1))
print("Symmetric Difference:", symmetric_difference)
print("Is Set 1 a subset of Set 2?", subset_check)
''',
26:
'''
color_dict = {'red':'#FF0000',
'green':'#008000',
'black':'#000000',
'white':'#FFFFFF'}
for key in sorted(color_dict):
    print("%s: %s" % (key, color_dict[key]))
''',
27:
'''
import itertools
def generate_combinations(dictionary):
    values = dictionary.values()
    combinations = list(itertools.product(*values))
    combinations = [''.join(comb) for comb in combinations]
    print(combinations)
    return combinations
def display_combinations(combinations):
    for comb in combinations:
        print(comb)
letters_dict = {
'key1': ['a', 'b', 'c'],
'key2': ['x', 'y', 'z'],
}
combinations = generate_combinations(letters_dict)
display_combinations(combinations)
''',
28:
'''
countries=['India','Russia','America','France','Germany','Pakistan']
cities=['Hyderabad','Moscow','Newyork','Paris','Berlin','Hyderabad']
z=list(zip(countries,cities))
d=dict(z)
print('{}----------{}'.format('Country', 'Capital'))
for k in d:
    print('{}----------{}'.format(k,d[k]))
''',
29:
'''
str=input("Enter any String:")
dict = {}
for x in str:
    dict[x]=dict.get(x,0)+1
for k,v in dict.items():
    print('key = {} \\t Its occurrences= {}'.format(k, v))
''',
30:
'''
Word=input("Enter the word to count")
with open('dict practice programs.txt', 'r') as file:
    content = file.read()
    occurrences = content.lower().count(Word.lower())
print(f"The word '{Word}' occurs {occurrences} time(s) in the file.")
''',
31:
'''
with open('file.txt', 'r') as fp1, open('file2.txt', 'r') as fp2:
    file1_contents = fp1.read()
    file2_contents = fp2.read()
if file1_contents == file2_contents:
    print("The files are identical.")
else:
    print("The files are different.")
''',
32:
'''
with open('file.txt', 'r') as f1, open("file2.txt",'r') as f2:
    contents1 = f1.read()
    contents2 = f2.read()
with open('file.txt', 'w') as f1, open("file2.txt", 'w') as f2:
    f1.write(contents2)
    f2.write(contents1)
print("Contents exchanged successfully.")
''',
33:
'''
with open('employee.txt', 'r') as file:
    record_count = 0
    for line in file:
        if line.strip(): # Check if line is not empty
            record_count += 1
print(f"Total number of records is: {record_count}")
''',
34:
'''
import sys
if len(sys.argv) != 4:
    print("Usage: python merge_files.py <file1> <file2> <output_file>")
else:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]
with open('file.txt', 'r') as f1, open("file2.txt", 'r') as f2, open("output.txt", 'w') as out_file:
    for line in f1:
        out_file.write(line)
    for line in f2:
        out_file.write(line)
print(f"Files '{file1}' and '{file2}' merged successfully into '{output_file}'.")
''',
35:
'''
import os,sys
fname=input("Enter filename: ")
if os.path.isfile(fname):
    f=open(fname,"r")
else:
    print("file does not exist")
    sys.exit()
countl=countw=countc=0
for line in f:
    words=line.split()
    countl=countl+1
    countw=countw+len(words)
    countc=countc+len(line)
print("No of lines",countl)
print("No of Words",countw)
print("No of Characters ",countc)
f.close()
''',

}

CQdata ={
1:
'''
WACP to illustrate Command-Line Arguments.
''',
2:
'''
WACP to illustrate the user-defined data type student.
''',
3:
'''
WACP to read the content of a given text file and count the number of characters, words and lines in it.

''',
4:
'''
WACP to read the content of a given text file, convert all lower case letters into upper case and display it on the screen

''',
5:
'''
WACP to copy the contents of one file into another
''',
6:
'''
WACP to implement Double Linked List 

''',
7:
'''
Stack Implementation using Linked List

''',
8:
'''
WACP to implement the following operations on  Binary Search Tree: Insertion, deletion, searching.

''',
9:
'''
WACP to perform traversals-preorder, inorder and  postorder on a Binary Search Tree (BST).

''',
10:
'''
WACP to implement all the List operations using Arrays

''',
11:
'''
WACP to write the record list of Student type into a binary file student.dat. Re-open the file, read the records from the file and display on the screen.

''',
12:
'''
WACP Linked list program for inserion and deletion
''',
13:
'''
Write a C program to implement all the List operations using Linked Lists.

''',
14:
'''
WAP to implement stack using array.
''',
15:
'''
WAP to implement queue using array.
''',
16:
'''
WAP to implement queue using Linked List.
''',
17:
'''
WAP to implement circular queue using array.
''',
18:
'''
WAP to convert infix expression to postfix using stack.
''',
19:
'''
WAP to implement postfix evaluation of an expression.
''',

}







CAdata ={
1:
'''
#include<stdio.h>
int main(int argc, char *argv[])
{
 int counter;
 printf("Program Name Is: %s",argv[0]);
 if(argc==1)
 printf("\\nNo Extra Command Line Argument Passed Other Than Program Name");
 if(argc>=2)
 {
 printf("\\nNumber Of Arguments Passed: %d",argc);
 printf("\\n----Following Are The Command Line Arguments Passed----");
 for(counter=0;counter<argc;counter++)
 printf("\\nargv[%d]: %s",counter,argv[counter]);
 }
 return 0;
}
''',
2:
'''
#include <stdio.h>
#include <string.h>
union student
{
 char name[20];
 char subject[20];
 float percentage;
};
int main()
{
 union student record1;
 union student record2;
 // assigning values to record1 union variable
 strcpy(record1.name, "Raju");
 strcpy(record1.subject, "Maths");
 record1.percentage = 86.50;
 printf("Union record1 values example\\n");
 printf(" Name : %s \\n", record1.name);
 printf(" Subject : %s \\n", record1.subject);
 printf(" Percentage : %f \\n\\n", record1.percentage);
 // assigning values to record2 union variable
 printf("Union record2 values example\\n");
 strcpy(record2.name, "Mani");
 printf(" Name : %s \\n", record2.name);
 strcpy(record2.subject, "Physics");
 printf(" Subject : %s \\n", record2.subject);
 record2.percentage = 99.50;
 printf(" Percentage : %f \\n", record2.percentage);
 return 0;
}

''',
3:
'''
#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[])
{
FILE *fp;
char ch;
int c=0, w=0, l=0;
if(argc!=2)
{
printf("Enter two arguments only");
exit(0);
}
fp=fopen(argv[1], "r");
if(fp==NULL)
{
printf("Unable to open file");
exit(0);
}
printf("\\nThe contents of the input file is:");
while((ch=fgetc(fp))!=EOF)
{
printf("%c", ch);
c++;
if(ch==' ' || ch=='\\n')
w++;
if(ch=='\\n')
l++;
}
printf("\\n No. of characters = %d \\n No. of words = %d \\n No. of lines = %d",c, w, l);
fclose(fp);
return 0;
}
''',
4:
'''
#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>
int main()
{
FILE *fp1, *fp2, *fp3;
char ch;
fp3= fopen("source.txt", "w");
fprintf(fp3,"the c programming this is an example of converting lower to upper");
fclose(fp3);
fp1 = fopen("source.txt", "r");
if (fp1 == NULL)
{
puts("File does not exist..");
exit(1);
}
fp2 = fopen("target.txt", "w");
if (fp2 == NULL)
{
puts("File does not exist..");
fclose(fp1);
exit(1);
}
while((ch=fgetc(fp1))!=EOF)
{
ch = toupper(ch);
fputc(ch,fp2);
}
fclose(fp1);
fclose(fp2);
printf("\\nContents of the Target File is:\\n");
fp2 = fopen("target.txt", "r"); 
while ((ch = getc(fp2)) != EOF)
printf("%c",ch);
printf("\\n");
fclose(fp2);
return 0;
}
''',
5:
'''
#include <stdio.h>
#include <stdlib.h> // For exit()

int main()
{
 FILE *fptr1, *fptr2;
 char file1[50], file2[50], c;

 printf("Enter the filename to open for reading \\n");
 scanf("%s", file1);

 // Open one file for reading
 fptr1 = fopen(file1, "r");
 if (fptr1 == NULL)
 {
 printf("Cannot open file %s \\n", file1);
 exit(0);
 }

 printf("Enter the filename to open for writing \\n");
 scanf("%s", file2);

 // Open another file for writing
 fptr2 = fopen(file2, "w");
 if (fptr2 == NULL)
 {
 printf("Cannot open file %s \\n", file2);
 exit(0);
 }

 // Read contents from file
 c = fgetc(fptr1);
 while (c != EOF)
 {
 fputc(c, fptr2);
 c = fgetc(fptr1);
}

 printf("\\nContents copied to %s", file2);

 fclose(fptr1);
 fclose(fptr2);
 return 0;
}
''',
6:
'''
#include<stdio.h>  
#include<stdlib.h>  
struct node  
{  
    struct node *prev;  
    struct node *next;  
    int data;  
};  
struct node *head;  
void insertion_beginning();  
void insertion_last();  
void insertion_specified();  
void deletion_beginning();  
void deletion_last();  
void deletion_specified();  
void display();  
void search();  
void main ()  
{  
int choice =0;  
    while(choice != 9)  
    {  
        printf("\\n*********Main Menu*********\\n");  
        printf("\\nChoose one option from the following list ...\\n");  
        printf("\\n===============================================\\n");  
        printf("\\n1.Insert in begining\\n2.Insert at last\\n3.Insert at any random location\\n4.Delete from Beginning\\n  5.Delete from last\\n6.Delete the node after the given data\\n7.Search\\n8.Show\\n9.Exit\\n");  
        printf("\\nEnter your choice?\\n");  
        scanf("\\n%d",&choice);  
        switch(choice)  
        {  
            case 1:  
            insertion_beginning();  
            break;  
            case 2:  
                    insertion_last();  
            break;  
            case 3:  
            insertion_specified();  
            break;  
            case 4:  
            deletion_beginning();  
            break;  
            case 5:  
            deletion_last();  
            break;  
            case 6:  
            deletion_specified();  
            break;  
            case 7:  
            search();  
            break;  
            case 8:  
            display();  
            break;  
            case 9:  
            exit(0);  
            break;  
            default:  
            printf("Please enter valid choice..");  
        }  
    }  
}  
void insertion_beginning()  
{  
   struct node *ptr;   
   int item;  
   ptr = (struct node *)malloc(sizeof(struct node));  
   if(ptr == NULL)  
   {  
       printf("\\nOVERFLOW");  
   }  
   else  
   {  
    printf("\\nEnter Item value");  
    scanf("%d",&item);  
      
   if(head==NULL)  
   {  
       ptr->next = NULL;  
       ptr->prev=NULL;  
       ptr->data=item;  
       head=ptr;  
   }  
   else   
   {  
       ptr->data=item;  
       ptr->prev=NULL;  
       ptr->next = head;  
       head->prev=ptr;  
       head=ptr;  
   }  
   printf("\\nNode inserted\\n");  
}  
     
}  
void insertion_last()  
{  
   struct node *ptr,*temp;  
   int item;  
   ptr = (struct node *) malloc(sizeof(struct node));  
   if(ptr == NULL)  
   {  
       printf("\\nOVERFLOW");  
   }  
   else  
   {  
       printf("\\nEnter value");  
       scanf("%d",&item);  
        ptr->data=item;  
       if(head == NULL)  
       {  
           ptr->next = NULL;  
           ptr->prev = NULL;  
           head = ptr;  
       }  
       else  
       {  
          temp = head;  
          while(temp->next!=NULL)  
          {  
              temp = temp->next;  
          }  
          temp->next = ptr;  
          ptr ->prev=temp;  
          ptr->next = NULL;  
          }  
             
       }  
     printf("\\nnode inserted\\n");  
    }  
void insertion_specified()  
{  
   struct node *ptr,*temp;  
   int item,loc,i;  
   ptr = (struct node *)malloc(sizeof(struct node));  
   if(ptr == NULL)  
   {  
       printf("\\n OVERFLOW");  
   }  
   else  
   {  
       temp=head;  
       printf("Enter the location");  
       scanf("%d",&loc);  
       for(i=0;i<loc;i++)  
       {  
           temp = temp->next;  
           if(temp == NULL)  
           {  
               printf("\\n There are less than %d elements", loc);  
               return;  
           }  
       }  
       printf("Enter value");  
       scanf("%d",&item);  
       ptr->data = item;  
       ptr->next = temp->next;  
       ptr -> prev = temp;  
       temp->next = ptr;  
       temp->next->prev=ptr;  
       printf("\\nnode inserted\\n");  
   }  
}  
void deletion_beginning()  
{  
    struct node *ptr;  
    if(head == NULL)  
    {  
        printf("\\n UNDERFLOW");  
    }  
    else if(head->next == NULL)  
    {  
        head = NULL;   
        free(head);  
        printf("\\nnode deleted\\n");  
    }  
    else  
    {  
        ptr = head;  
        head = head -> next;  
        head -> prev = NULL;  
        free(ptr);  
        printf("\\nnode deleted\\n");  
    }  
  
}  
void deletion_last()  
{  
    struct node *ptr;  
    if(head == NULL)  
    {  
        printf("\\n UNDERFLOW");  
    }  
    else if(head->next == NULL)  
    {  
        head = NULL;   
        free(head);   
        printf("\\nnode deleted\\n");  
    }  
    else   
    {  
        ptr = head;   
        while(ptr->next != NULL)  
        {  
            ptr = ptr -> next;   
        }  
        ptr -> prev -> next = NULL;   
        free(ptr);  
        printf("\\nnode deleted\\n");  
    }  
}  
void deletion_specified()  
{  
    struct node *ptr, *temp;  
    int val;  
    printf("\\n Enter the data after which the node is to be deleted : ");  
    scanf("%d", &val);  
    ptr = head;  
    while(ptr -> data != val)  
    ptr = ptr -> next;  
    if(ptr -> next == NULL)  
    {  
        printf("\\nCan't delete\\n");  
    }  
    else if(ptr -> next -> next == NULL)  
    {  
        ptr ->next = NULL;  
    }  
    else  
    {   
        temp = ptr -> next;  
        ptr -> next = temp -> next;  
        temp -> next -> prev = ptr;  
        free(temp);  
        printf("\\nnode deleted\\n");  
    }     
}  
void display()  
{  
    struct node *ptr;  
    printf("\\n printing values...\\n");  
    ptr = head;  
    while(ptr != NULL)  
    {  
        printf("%d\\n",ptr->data);  
        ptr=ptr->next;  
    }  
}   
void search()  
{  
    struct node *ptr;  
    int item,i=0,flag;  
    ptr = head;   
    if(ptr == NULL)  
    {  
        printf("\\nEmpty List\\n");  
    }  
    else  
    {   
        printf("\\nEnter item which you want to search?\\n");   
        scanf("%d",&item);  
        while (ptr!=NULL)  
        {  
            if(ptr->data == item)  
            {  
                printf("\\nitem found at location %d ",i+1);  
                flag=0;  
                break;  
            }   
            else  
            {  
                flag=1;  
            }  
            i++;  
            ptr = ptr -> next;  
        }  
        if(flag==1)  
        {  
            printf("\\nItem not found\\n");  
        }  
    }     
          
}

''',
7:
'''
#include <stdio.h>
#include <stdlib.h>

// Structure to create a node with data and the next pointer
struct node {
    int info;
    struct node *ptr;
}*top,*top1,*temp;

int count = 0;
// Push() operation on a  stack
void push(int data) {
     if (top == NULL)
    {
        top =(struct node *)malloc(1*sizeof(struct node));
        top->ptr = NULL;
        top->info = data;
    }
    else
    {
        temp =(struct node *)malloc(1*sizeof(struct node));
        temp->ptr = top;
        temp->info = data;
        top = temp;
    }
    count++;
    printf("Node is Inserted\\n\\n");
}

int pop() {
     top1 = top;
 
    if (top1 == NULL)
    {
        printf("\\nStack Underflow\\n");
        return -1;
    }
    else
        top1 = top1->ptr;
    int popped = top->info;
    free(top);
    top = top1;
    count--;
    return popped;
}

void display() {
    // Display the elements of the stack
    top1 = top;
 
    if (top1 == NULL)
    {
        printf("\\nStack Underflow\\n");
        return;
    }
    
    printf("The stack is \\n");
    while (top1 != NULL)
    {
        printf("%d--->", top1->info);
        top1 = top1->ptr;
    }
    printf("NULL\\n\\n");

}

int main() {
    int choice, value;
    printf("\\nImplementation of Stack using Linked List\\n");
    while (1) {
        printf("\\n1. Push\\n2. Pop\\n3. Display\\n4. Exit\\n");
        printf("\\nEnter your choice : ");
        scanf("%d", &choice);
        switch (choice) {
        case 1:
            printf("\\nEnter the value to insert: ");
            scanf("%d", &value);
            push(value);
            break;
        case 2:
            printf("Popped element is :%d\\n", pop());
            break;
        case 3:
            display();
            break;
        case 4:
            exit(0);
            break;
        default:
            printf("\\nWrong Choice\\n");
        }
    }
}

''',
8:
'''
#include <stdio.h>
#include <stdlib.h>
struct Node {
    int data;
    struct Node *left, *right;
};
struct Node *root = NULL;
struct Node* newNode(int item)
{
    struct Node* temp = (struct Node*)malloc(sizeof(struct Node));
    temp->data = item;
    temp->left = temp->right = NULL;
    return temp;
}
void inorder(struct Node* root)
{
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}
void insert(int data){
   struct Node *tempNode = (struct Node*) malloc(sizeof(struct Node));
   struct Node *current;
   struct Node *parent;
   tempNode->data = data;
   tempNode->left = NULL;
   tempNode->right = NULL;

   //if tree is empty
   if(root == NULL) {
      root = tempNode;
   } else {
      current = root;
      parent = NULL;
      while(1) {
         parent = current;

         //go to left of the tree
         if(data < parent->data) {
            current = current->left;

            //insert to the left
            if(current == NULL) {
               parent->left = tempNode;
               return;
            }
         }//go to right of the tree
         else {
            current = current->right;
            
            //insert to the right
            if(current == NULL) {
               parent->right= tempNode;
               return;
            }
         }
      }
   }
}

struct Node* deleteNode(struct Node* root, int k)
{
    // Base case
    if (root == NULL)
        return root;
 
    // Recursive calls for ancestors of
    // node to be deleted
    if (root->data > k) {
        root->left = deleteNode(root->left, k);
        return root;
    }
    else if (root->data < k) {
        root->right = deleteNode(root->right, k);
        return root;
    }
 
    // We reach here when root is the node
    // to be deleted.
 
    // If one of the children is empty
    if (root->left == NULL) {
        struct Node* temp = root->right;
        free(root);
        return temp;
    }
    else if (root->right == NULL) {
        struct Node* temp = root->left;
        free(root);
        return temp;
    }
 
    // If both children exist
    else {
 
        struct Node* succParent = root;
 
        // Find successor
        struct Node* succ = root->right;
        while (succ->left != NULL) {
            succParent = succ;
            succ = succ->left;
        }
 
        if (succParent != root)
            succParent->left = succ->right;
        else
            succParent->right = succ->right;
 
        // Copy Successor Data to root
        root->data = succ->data;
 
        // Delete Successor and return root
        free(succ);
        return root;
    }
}
 
struct Node* search(int data)
{
   struct Node *current = root;
   printf("\\n\\nVisiting elements:\\n ");
   while(current->data != data) {
      if(current != NULL) {
         printf("%d ",current->data);
         
         //go to left tree
         if(current->data > data) {
            current = current->left;
         }//else go to right tree
         else {
            current = current->right;
         }
         
         if(current == NULL) {
            return NULL;
         }
      }
   }
   return current;
}

int main(){
  
   insert(55);
   insert(20);
   insert(90);
   insert(50);
   insert(35);
   insert(15);
   insert(65);
   printf("Given Data Inserted\\n");
   
   printf("Original BST: ");
   inorder(root);
   
   printf("\\n\\nDelete a Leaf Node: 15\\n");
    root = deleteNode(root, 15);
    printf("Modified BST tree after deleting Leaf Node:\\n");
    inorder(root);
 
    printf("\\n\\nDelete Node with single child: 90\\n");
    root = deleteNode(root, 90);
    printf("Modified BST tree after deleting single child Node:\\n");
    inorder(root);
 
    printf("\\n\\nDelete Node with both child: 55\\n");
    root = deleteNode(root, 55);
    printf("Modified BST tree after deleting both child Node:\\n");
    inorder(root);
        
    struct Node* k;
   k = search(35);
   if(k != NULL)
      printf("\\nElement %d found", k->data);
   else
      printf("\\nElement not found");
     
   return 0;
}

''',
9:
'''
#include <stdio.h>
#include <stdlib.h>
struct node {
   int data;
   struct node *leftChild;
   struct node *rightChild;
};
struct node *root = NULL;
void insert(int data){
   struct node *tempNode = (struct node*) malloc(sizeof(struct node));
   struct node *current;
   struct node *parent;
   tempNode->data = data;
   tempNode->leftChild = NULL;
   tempNode->rightChild = NULL;

//if tree is empty
   if(root == NULL) {
      root = tempNode;
   } else {
      current = root;
      parent = NULL;
      while(1) {
         parent = current;

         //go to left of the tree
         if(data < parent->data) {
            current = current->leftChild;

            //insert to the left
            if(current == NULL) {
               parent->leftChild = tempNode;
               return;
            }
         }//go to right of the tree
         else {
            current = current->rightChild;

            //insert to the right
            if(current == NULL) {
               parent->rightChild = tempNode;
               return;
            }
         }
      }
   }
}
void pre_order_traversal(struct node* root){
   if(root != NULL) {
      printf("%d ",root->data);
      pre_order_traversal(root->leftChild);
      pre_order_traversal(root->rightChild);
   }
}
void inorder_traversal(struct node* root){
   if(root != NULL) {
      inorder_traversal(root->leftChild);
      printf("%d ",root->data);
      inorder_traversal(root->rightChild);
   }
}
void post_order_traversal(struct node* root){
   if(root != NULL) {
      post_order_traversal(root->leftChild);
      post_order_traversal(root->rightChild);
      printf("%d ", root->data);
   }
}

int main(){
   int i;
   int array[7] = { 27, 14, 35, 10, 19, 31, 42 };
   for(i = 0; i < 7; i++)
      insert(array[i]);
   printf("\\nPreorder traversal: ");
   pre_order_traversal(root);
   printf("\\nInorder traversal: ");
   inorder_traversal(root);
   printf("\\nPost order traversal: ");
   post_order_traversal(root);
   return 0;
}

''',
10:
'''
#include<stdio.h>
#include<stdlib.h>
#define LIST_SIZE 30
int main()
{
int *element=NULL;
int ch,i,j,n;
int insdata,deldata,moddata,found;
int top=-1;
element=(int*)malloc(sizeof(int)* LIST_SIZE);
while(1)
{
fflush(stdin);
printf("\\n\\n basic Operations in a Linear List......");
printf("\\n 1.Create New List \\t 2.Modify List \\t 3.View List");
printf("\\n 4.Insert First \\t 5.Insert Last \\t 6.Insert Middle");
printf("\\n 7.Delete First \\t 8.Delete Last \\t 9.Delete Middle");
printf("\\nEnter the Choice 1 to 10 : ");
scanf("%d",&ch);
switch(ch)
{
case 1:
top=-1;
printf("\\n Enter the Limit (How many Elements):");
scanf("%d",&n);
for(i=0;i<n;i++)
{
printf("\\n Enter The Element [%d]:",(i+1));
scanf("%d",&element[++top]);
}
break;
case 2:
if(top==-1)
{
printf("\\n Linear List is Empty:");
break;
}
printf("\\n Enter the Element for Modification:");
scanf("%d",&moddata);
found=0;
for(i=0;i<=top;i++)
{
if(element[i]==moddata)
{
found=1;
printf("\\n Enter The New Element :");
scanf("%d",&element[i]);
break;
}
}
if(found==0)
printf("\\n Element %d not found",moddata);
break;
case 3:
if(top==-1)
printf("\\n \\n Linear List is Empty:");
else if(top==LIST_SIZE -1)
printf("\\n Linear LIst is Full:");
for(i=0;i<=top;i++)
printf("\\n Element[%d]is-->%d",(i+1),element[i]);
break;
case 4:
if(top==LIST_SIZE-1)
{
printf("\\n Linear List is Full:");
break;
}
top++;
for(i=top;i>0;i--)
element[i]=element[i-1];
printf("\\n Enter the Element:");
scanf("%d",&element[0]);
break;
case 5:
if(top==LIST_SIZE-1)
{
printf("\\n Linear List is Full:");
break;
}
printf("\\n Enter the Element:");
scanf("%d",&element[++top]);
break;
case 6:
if(top==LIST_SIZE-1)
printf("\\n Linear List is Full:");
else if(top==-1)
printf("\\n linear List is Empty.");
else
{
found=0;
printf("\\n Enter the Element after which the insertion is to be made:");
scanf("%d",&insdata);
for(i=0;i<=top;i++)
if(element[i]==insdata)
{
found=1;
top++;
for(j=top;j>i;j--)
element[j]=element[j-1];
printf("\\n Enter the Element :");
scanf("%d",&element[i+1]);
break;
}
if(found==0)
printf("\\n Element %d Not Found",insdata);
}
break;
case 7:
if(top==-1)
{
printf("\\n Linear List is Empty:");
break;
}
printf("\\n Deleted Data-->Element :%d",element[0]);
top--;
for(i=0;i<=top;i++)
element[i]=element[i+1];
break;
case 8:
if(top==-1)
printf("\\n Linear List is Empty:");
else
printf("\\n Deleted Data-->Element :%d",element[top--]);
break;
case 9:
if(top==-1)
{
printf("\\n Linear List is Empty:");
break;
}
printf("\\n Enter the Element for Deletion :");
scanf("%d",&deldata);
found=0;
for(i=0;i<=top;i++)
if(element[i]==deldata)
{
found=1;
printf("\\n Deleted data-->Element :%d",element[i]);
top--;
for(j=i;j<=top;j++)
element[j]=element[j+1];
break;
}
if(found==0)
printf("\\n Element %d Not Found ",deldata);
break;
default: 
free(element);
printf("\\n End Of Run Of Your Program.........");
exit(0);
}
}
}

''',
11:
'''
#include <stdio.h>
struct student
{
char name[50];
int rollno;
float avg;
};
int main()
{
struct student a[10], b[10];
FILE *fptr;
int i, n;
fptr=fopen("student.dat","wb");
printf("\\nEnter the Number of Students:");
scanf("%d", &n);
for (i=0; i<n; i++)
{
fflush(stdin);
printf("\\nEnter Student %d Information", i+1);
printf("\\nEnter name: ");
scanf("%s", a[i].name);
printf("\\nEnter Roll No: ");
scanf("%d",&a[i].rollno);
printf("\\nEnter Average Mark: ");
scanf("%f",&a[i].avg);
}
fwrite(a,sizeof(a),1,fptr);
fclose(fptr);
fptr=fopen("student.dat","rb");
fread(b,sizeof(b),1,fptr);
printf("\\nThe Student Records present in the File are:");

for (i=0; i<n; i++)
{
printf("\\nName: %s\\t\\tRoll No: %d\\t\\tAverage Mark: %f\\n", b[i].name,b[i].rollno, b[i].avg);
}
fclose(fptr);
}

''',
12:
'''
#include<stdio.h>  
#include<stdlib.h>  
struct node   
{  
    int data;  
    struct node *next;   
};  
struct node *start;  
               /*fuction declaration of all the operations*/
void insert_begin();   
void insert_last();  
void insert_locc();  
void delete_begin();  
void delete_last();  
void delete_locc();  
void print();  
void main ()  
{  
    int ch=0;  
    while(ch!=8)   
    {    
        printf("\\nEnter the operation to be performed\\n");    
        printf("\\n1.Insert in the begining\\n2.Insert at last\\n3.Insert at any specified position\\n4.Delete from Beginning\\n5.Delete from last\\n6.Delete node after specified location\\n7.Show\\n8.Exit\\n");           
        scanf("\\n%d",&ch);  
        switch(ch)  
        {        /*function calls of all the operations */
            case 1:  
            insert_begin();       
            break;  
            case 2:  
            insert_last();         
            break;  
            case 3:  
            insert_locc();       
            break;  
            case 4:  
            delete_begin();       
            break;  
            case 5:  
            delete_last();        
            break;  
            case 6:  
            delete_locc();           
            break;  
            case 7:  
            print();        
            break;  
            case 8:  
            exit(0);  
            break;  
            default:  
            printf("Enter valid option");  
        }  
    }  
}           /*function definition*/
void insert_begin()                  //to insert the node at the beginnning of linked list
{  
    struct node *p;  
    int value;  
    p=(struct node *) malloc(sizeof(struct node *));  
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");  
    }  
    else  
    {  
        printf("\\nEnter value\\n");    
        scanf("%d",&value);    
        p->data=value;  
        p->next=start;  
        start=p;  
    }  
}  
void insert_last()                //to insert the node at the last of linked list
{  
    struct node *p,*temp;  
    int value;     
    p=(struct node*)malloc(sizeof(struct node));      
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");     
    }  
    else  
    {  
        printf("\\nEnter value\\n");  
        scanf("%d",&value);  
        p->data=value;  
        if(start==NULL)  
        {  
            p->next=NULL;  
            start=p;  
        }  
        else  
        {  
            temp=start;  
            while(temp->next!=NULL)  
            {  
                temp=temp->next;  
            }  
            temp->next=p;  
            p->next=NULL;  
        }  
    }  
}  
void insert_locc()               //to insert the node at the specified location of linked list
{  
    int i,loc,value;   
    struct node *p, *temp;  
    p=(struct node *)malloc(sizeof(struct node));  
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");  
    }  
    else  
    {  
        printf("\\nEnter element value");  
        scanf("%d",&value);  
        p->data=value;  
        printf("\\nEnter the location after which you want to insert ");  
        scanf("\\n%d",&loc);  
        temp=start;  
        for(i=0;i<loc;i++)  
        {  
            temp=temp->next;  
            if(temp==NULL)  
            {  
                printf("\\ncan't insert\\n");  
                return;  
            }  
        }  
        p->next=temp->next;   
        temp->next=p; 
    }  
}  
void delete_begin()          //to delete the node present in the beginning of the linked list
{  
    struct node *p;  
    if(start==NULL)  
    {  
        printf("\\nList is empty\\n");  
    }  
    else   
    {  
        p=start;  
        start=p->next;  
        free(p);  
    }  
}  
void delete_last()          //to delete the node present in the last of the linked list
{  
    struct node *p,*p1;  
    if(start==NULL)  
    {  
        printf("\\nlist is empty");  
    }  
    else if(start->next==NULL)  
    {  
        start=NULL;  
        free(start);  
        printf("\\nOnly node of the list deleted ...\\n");  
    }  
    else  
    {  
        p=start;   
        while(p->next!=NULL)  
        {  
            p1=p;  
            p=p->next;  
        }  
        p1->next=NULL;  
        free(p);  
    }     
}  
void delete_locc()    //to delete the node present at the specified of the linked list
{  
    struct node *p,*p1;  
    int loc,i;    
    printf("\\n Enter the location of the node after which you want to perform deletion \\n");  
    scanf("%d",&loc);  
    p=start;  
    for(i=0;i<loc;i++)  
    {  
        p1=p;       
        p=p->next;  
           
        if(p==NULL)  
        {  
            printf("\\nCan't delete");  
            return;  
        }  
    }  
    p1->next=p->next;  
    free(p);  
    printf("\\nDeleted node %d ",loc+1);  
}  
void print()    //to print the values in the linked list
{  
    struct node *p;  
    p=start;   
    if(p==NULL)  
    {  
        printf("Nothing to print");  
    }  
    else  
    {  
        printf("\\nprinting values\\n");   
        while (p!=NULL)  
        {  
            printf("%d ",p->data);  
            p=p->next;  
        }  
    }  
}     

''',
13:
'''
#include<stdio.h>  
#include<stdlib.h>  
struct node   
{  
    int data;  
    struct node *next;   
};  
struct node *start;  
               /*fuction declaration of all the operations*/
void insert_begin();   
void insert_last();  
void insert_locc();  
void delete_begin();  
void delete_last();  
void delete_locc();  
void Search();
void print();  
void main ()  
{  
    int ch=0;  
    while(1)   
    {    
        printf("\\nEnter the operation to be performed\\n");    
        printf("\\n1.Insert in the begining\\n2.Insert at last\\n3.Insert at any specified position\\n4.Delete from Beginning\\n5.Delete from last\\n6.Delete node after specified location\\n7.Search()\\n8.Show\\n9.Exit\\n");           
        scanf("\\n%d",&ch);  
        switch(ch)  
        {        /*function calls of all the operations */
            case 1:  
            insert_begin();       
            break;  
            case 2:  
            insert_last();         
            break;  
            case 3:  
            insert_locc();       
            break;  
            case 4:  
            delete_begin();       
            break;  
            case 5:  
            delete_last();        
            break;  
            case 6:  
            delete_locc();           
            break;  
            case 7:
            search();
            break; 
            case 8:  
            print();        
            break;  
            default: 
            printf("\\n End Of Run Of Your Program.........");
            exit(0);

        }  
    }  
}           /*function definition*/
void insert_begin()                  //to insert the node at the beginnning of linked list
{  
    struct node *p;  
    int value;  
    p=(struct node *) malloc(sizeof(struct node *));  
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");  
    }  
    else  
    {  
        printf("\\nEnter value\\n");    
        scanf("%d",&value);    
        p->data=value;  
        p->next=start;  
        start=p;  
    }  
}  
void insert_last()                //to insert the node at the last of linked list
{  
    struct node *p,*temp;  
    int value;     
    p=(struct node*)malloc(sizeof(struct node));      
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");     
    }  
    else  
    {  
        printf("\\nEnter value\\n");  
        scanf("%d",&value);  
        p->data=value;  
        if(start==NULL)  
        {  
            p->next=NULL;  
            start=p;  
        }  
        else  
        {  
            temp=start;  
            while(temp->next!=NULL)  
            {  
                temp=temp->next;  
            }  
            temp->next=p;  
            p->next=NULL;  
        }  
    }  
}  
void insert_locc()               //to insert the node at the specified location of linked list
{  
    int i,loc,value;   
    struct node *p, *temp;  
    p=(struct node *)malloc(sizeof(struct node));  
    if(p==NULL)  
    {  
        printf("\\nOVERFLOW");  
    }  
    else  
    {  
        printf("\\nEnter element value");  
        scanf("%d",&value);  
        p->data=value;  
        printf("\\nEnter the location after which you want to insert ");  
        scanf("\\n%d",&loc);  
        temp=start;  
        for(i=0;i<loc;i++)  
        {  
            temp=temp->next;  
            if(temp==NULL)  
            {  
                printf("\\ncan't insert\\n");  
                return;  
            }  
        }  
        p->next=temp->next;   
        temp->next=p; 
    }  
}  
void delete_begin()          //to delete the node present in the beginning of the linked list
{  
    struct node *p;  
    if(start==NULL)  
    {  
        printf("\\nList is empty\\n");  
    }  
    else   
    {  
        p=start;  
        start=p->next;  
        free(p);  
    }  
}  
void delete_last()          //to delete the node present in the last of the linked list
{  
    struct node *p,*p1;  
    if(start==NULL)  
    {  
        printf("\\nlist is empty");  
    }  
    else if(start->next==NULL)  
    {  
        start=NULL;  
        free(start);  
        printf("\\nOnly node of the list deleted ...\\n");  
    }  
    else  
    {  
        p=start;   
        while(p->next!=NULL)  
        {  
            p1=p;  
            p=p->next;  
        }  
        p1->next=NULL;  
        free(p);  
    }     
}  
void delete_locc()    //to delete the node present at the specified of the linked list
{  
    struct node *p,*p1;  
    int loc,i;    
    printf("\\n Enter the location of the node after which you want to perform deletion \\n");  
    scanf("%d",&loc);  
    p=start;  
    for(i=0;i<loc;i++)  
    {  
        p1=p;       
        p=p->next;  
           
        if(p==NULL)  
        {  
            printf("\\nCan't delete");  
            return;  
        }  
    }  
    p1->next=p->next;  
    free(p);  
    printf("\\nDeleted node %d ",loc+1);  
}  
void search()
{
    int found = -1;
    // creating node to traverse
    struct node* tr = start;
 
    // first checking if the list is empty or not
    if (start == NULL) {
        printf("Linked list is empty\\n");
    }
    else {
        printf("\\nEnter the element you want to search: ");
        int key;
        scanf("%d", &key);
 
        // checking by traversing
        while (tr != NULL) {
            // checking for key
            if (tr->data == key) {
                found = 1;
                break;
            }
            // moving forward if not at this position
            else {
                tr = tr->next;
            }
        }
 
        // printing found or not
        if (found == 1) {
            printf(
                "Yes, %d is present in the linked list.\\n",
                key);
        }
        else {
            printf("No, %d is not present in the linked "
                   "list.\\n",
                   key);
        }
    }
}

void print()    //to print the values in the linked list
{  
    struct node *p;  
    p=start;   
    if(p==NULL)  
    {  
        printf("Nothing to print");  
    }  
    else  
    {  
        printf("\\nprinting values\\n");   
        while (p!=NULL)  
        {  
            printf("%d ",p->data);  
            p=p->next;  
        }  
    }  
}     

''',
14:
'''
#include< stdio.h>
#include< stdlib.h>
#define MAX_SIZE 10
void push();
void pop();
void display();
int stack[MAX_SIZE],top=-1;
void main()
{
    int choice;
    while(1)
    {
        printf("1.Push\\t2.Pop\\t3.Display\\t4.Exit\\n");
        printf("Enter your choice:");
        scanf("%d",&choice);
        switch(choice)
        {
            case 1:
                push();
                break;
            case 2:
                pop();
                break;
            case 3:
                display();
                break;
            case 4:
                exit(0);
                break;
            default:
                printf("Enter valid choice\\n");
        }
    }
}
int isfull()
{
    return top==MAX_SIZE;
}
int isempty()
{
    return top==-1;
}
void push()
{
    int value;
    if(isfull())
        printf("StackOverflow\\n");
    else
    {
        printf("Enter the value:");
        scanf("%d",&value);
        top++;
        stack[top]=value;
    }
}
void pop()
{
    if(isempty())
        printf("Stack is empty\\n");
    else
        top--;
}
void display()
{
    if(isempty())
        printf("Stack is empty\\n");
    else
    {
        for(int i=top;i>=0;i--)
            printf("%d ",stack[i]);
        printf("\\n");
    }
}
    
''',
15:
'''
#include< stdio.h>
#include< stdlib.h>
#define MAX_CAPACITY 10
int queue[MAX_CAPACITY];
int front=-1,rear=-1;
void enQueue();
void deQueue();
void display();
int isfull()
{
    return rear==MAX_CAPACITY-1;
}
int isempty()
{
    return (front==-1 || front>rear);
}
void main()
{
    int choice;
    while(1)
    {
        printf("1.Enqueue\\t2.Dequeue\\t3.Display\\t4.Exit\\n");
        printf("Enter your Choice:");
        scanf("%d",&choice);
        switch(choice)
        {
            case 1:
                enQueue();
                break;
            case 2:
                deQueue();
                break;
            case 3:
                display();
                break;
            case 4:
                exit(0);
                break;
            default:
                printf("Enter valid Choice\\n");
        }
    }
}
void enQueue()
{
    if(isfull())
        printf("Queue is full\\n");
    else
    {
        if(front==-1)
            front=0;
        int value;
        printf("Enter the value:");
        scanf("%d",&value);
        rear++;
        queue[rear]=value;
    }
}
void deQueue()
{
    if(isempty())
        printf("Queue is empty\\n");
    else
        front++;
}
void display()
{
    if(isempty())
        printf("Queue is empty\\n");
    else
    {
        for(int i=front;i<=rear;i++)
            printf("%d ",queue[i]);
        printf("\\n");
    }
}
    
''',
16:
'''
#include< stdio.h>
#include< stdlib.h>
struct node{
    int data;
    struct node *next;
};
struct node *front=NULL;
struct node *rear=NULL;
void enQueue();
void deQueue();
void display();
void main()
{
    int choice;
    while(1)
    {
        printf("1.Enqueue\\t2.Dequeue\\t3.Display\\t4.Exit\\n");
        printf("Enter your choice:");
        scanf("%d",&choice);
        switch(choice)
        {
            case 1:
                enQueue();
                break;
            case 2:
                deQueue();
                break;
            case 3:
                display();
                break;
            case 4:
                exit(0);
                break;
            default:
                printf("Enter valid choice\\n");
        }
    }
}
void enQueue()
{
    struct node *p;
    p=(struct node *)malloc(sizeof(struct node));
    if(p==NULL)
        printf("OVERFLOW\\n");
    else
    {
        int value;
        printf("Enter the value:");
        scanf("%d",&value);
        p->data=value;
        p->next=NULL;
        if(front==NULL)
            front=rear=p;
        else
        {
            rear->next=p;
            rear=p;
            rear->next=NULL;
        }
    }
}
void deQueue()
{
    if(front==NULL)
        printf("Queue is empty\\n");
    else
        front=front->next;
}
void display()
{
    if(front==NULL)
        printf("Queue is empty\\n");
    else
    {
        struct node *temp;
        temp=front;
        while(temp!=NULL)
        {
            printf("%d ",temp->data);
            temp=temp->next;
        }
        printf("\\n");
    }
}
    
''',
17:
'''
#include< stdio.h>
#include< stdlib.h>
#define size 8
int queue[size];
int front=-1,rear=-1;
void enQueue();
void deQueue();
void display();
 void main()
 {
     int choice;
     while(1)
     {
         printf("1.Enqueue\\t2.Dequeue\\t3.Display\\t4.Exit\\n");
         printf("Enter your choice:");
         scanf("%d",&choice);
         switch(choice)
         {
             case 1:
                 enQueue();
                 break;
             case 2:
                 deQueue();
                 break;
             case 3:
                 display();
                 break;
             case 4:
                 exit(0);
                 break;
             default:
                 printf("Enter valid choice\\n");
         }
     }
 }
 void enQueue()
 {
     if((front==0 && rear==size-1)|| front==rear+1)
         printf("Queue is full\\n");
     if(front==-1)
     {
         front++;
         rear++;
     }
     else
     {
         if(rear==size-1)
             rear=0;
         else
             rear++;
     }
     printf("Enter the value:");
     scanf("%d",&queue[rear]);
 }
 void deQueue()
 {
     if(front==-1)
         printf("Queue is empty\\n");
     else
     {
         if(front==rear)
         {
             front=-1;
             rear=-1;
         }
         else
         {
             if(front==size-1)
                 front=0;
             else
                 front++;
         }
     }
 }
 void display()
 {
     if(front==-1)
         printf("Queue is empty\\n");   
     else
     {
         int i;
         if(front<=rear)
         {
             for(i=front;i<=rear;i++)
                 printf("%d ",queue[i]);
             printf("\\n");
         }
         else
         {
             for(i=front;i< size;i++)
                 printf("%d ",queue[i]);
             for(i=0;i<=rear;i++)
                 printf("%d ",queue[i]);
             printf("\\n");
         }
     }
 }
    
''',
18:
'''
#include< stdio.h>
#define MAX_SIZE 20
char stk[20];
int top=-1;
int isEmpty()
{
    return top==-1;
}
int isFull()
{
    return top==MAX_SIZE-1;
}
char peek()
{
    return stk[top];
}
char pop()
{
    if(isEmpty())
        return -1;
    char ch=stk[top];
    top--;
    return(ch);
}
void push(char oper)
{
    if(isFull())
        printf("StackOverflow\\n");
    else
        {
            top++;
            stk[top]=oper;
        }
}
int checkifoperand(char ch)
{
    return (ch>='a' && ch<='z')||(ch>='A' && ch<='Z');
}
int precedence(char ch)
{
    switch(ch)
    {
        case '+':
        case '-':
            return 1;
            break;
        case '*':
        case '/':
            return 2;
            break;
        case '^':
            return 3;
            break;
    }
    return -1;
}
int convertinfixtopostfix(char *expression)
{
    int i,j;
    for(i=0,j=-1;expression[i];i++)
    {
        if(checkifoperand(expression[i]))
            expression[++j]=expression[i];
        else if(expression[i]=='(')
            push(expression[i]);
        else if(expression[i]==')')
        {
            while(!isEmpty() && peek()!='(')
                expression[++j]=pop();
            if(!isEmpty() && peek()!='(')
                return -1;
                
            else
                pop();
        }
        else
        {
            while(!isEmpty() && precedence(expression[i])<=precedence(peek()))
                expression[++j]=pop();
            push(expression[i]);
        }
    }
    while(!isEmpty())
        expression[++j]=pop();
    expression[++j]='\0';
    printf("%s\\n",expression);
}
int main()
{
    char expression[MAX_SIZE];
    printf("Enter expression:");
    scanf("%[^\\n]s",expression);
    convertinfixtopostfix(expression);
    return 0;
}
            
''',
19:
'''
#include< stdio.h>
int stack[20];
int top = -1;

void push(int x)
{
    stack[++top] = x;
}

int pop()
{
    return stack[top--];
}

int main()
{
    char exp[20];
    char *e;
    int n1,n2,n3,num;
    printf("Enter the expression :: ");
    scanf("%s",exp);
    e = exp;
    while(*e != '\0')
    {
        if(isdigit(*e))
        {
            num = *e - 48;
            push(num);
        }
        else
        {
            n1 = pop();
            n2 = pop();
            switch(*e)
            {
            case '+':
            {
                n3 = n1 + n2;
                break;
            }
            case '-':
            {
                n3 = n2 - n1;
                break;
            }
            case '*':
            {
                n3 = n1 * n2;
                break;
            }
            case '/':
            {
                n3 = n2 / n1;
                break;
            }
            }
            push(n3);
        }
        e++;
    }
    printf("\\nThe result of expression %s  =  %d\\n\\n",exp,pop());
    return 0;
}

''',
}




assert len(pythonAdata) == len(pythonQdata)
def displayP():
    for keys,values in pythonQdata.items():
        print('-----------------------------------------------------------------------')
        try:
            print(keys,'==>',values)
        except Exception as e:
            print(e)
    print('------------------------------------------------------------------------')

assert len(CAdata) == len(CQdata)
def displayC():
    for keys,values in CQdata.items():
        print('-----------------------------------------------------------------------')
        try:
            print(keys,'==>',values)
        except Exception as e:
            print(e)
    print('------------------------------------------------------------------------')

def run():
    try:
        while True:
            sub = str(input('enter the subject (python or c) >>>')).lower()
            if sub == 'python':
                displayP()
                print('\n enter 69 to exit to other subject \n')
                while True:
                    try:
                        qnum = int(input('enter the question number >>>'))
                        if qnum==69:
                            break
                    except Exception as e :
                        print('enter number only')
                        continue
                    print('--------------------------------------------------------------------------')
                    print(pythonAdata[qnum])
                    print('--------------------------------------------------------------------------')
            if sub == 'c':
                displayC()
                print('\n enter 69 to exit to subject \n')
                while True:
                    try:
                        qnum = int(input('enter the question number >>>'))
                        if qnum==69:
                            break
                    except Exception as e :
                        print('enter number only')
                        continue
                    print('--------------------------------------------------------------------------')
                    print(CAdata[qnum])
                    print('--------------------------------------------------------------------------')


    except Exception as e:
        print(e)
        print('unknown error occured')
        run()
try:
    run()
except Exception as e :
    print(e)
