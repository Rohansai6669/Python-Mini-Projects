import streamlit as st
st.title("FLAMES GAME")

s1=st.text_input("Enter first name:")
s2=st.text_input("Enter second name:")
temp1=[]
count=0
for i in s1:
    if i in s2 and i not in temp1:
        continue
    else:
        count+=1
        
temp3=[]
for i in s2:
    if i in s1 and i not in temp3:
        continue
    else:
        count+=1
s="flames"
l=["Friends","Lovers","Affection","Marriage","Enemies","Siblings"]
dict1=dict(zip(s,l))
while(len(s)!=1):
   i=count%len(s)-1
   if i==-1:
       s=s[:len(s)-1]
   else:
       s=s[i+1:]+s[:i]
if (st.button("SUBMIT")):
    st.success(dict1[s])