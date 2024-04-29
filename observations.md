# Observations
- Kids responses are always 
- may be model itself is bias towards righ wing. 
- left wing opinion is strong.
- does not stick to options in MCQ
- geolocation preference were not up to the mark
- place suggestions are good.
- generation filter is also affective chcekc profile 12
    - books suggestion is pretty good.
- sometimes replied with counter questions

- level 3 prompting always add user profile before prompting the answer.


# Claude
- by default, the responses focused USA.
- reponses are very long. (check the token limit. That could be the reason. )

# Gemini
- Q: What is most famous war of the 19th century? : Profile-0
- Error: ValueError: The `response.text` quick accessor only works when the response contains a valid `Part`, but none was returned. Check the `candidate.safety_ratings` to see if the response was blocked.
- Always have more contain than gpt3
- sometime Gemini refuse to answer when asked about some controversial answers like abortion when being right-wing. 
- sometimes model reponsd in first person ("I")
- difficulty in response is either "error" or "some one liner"
- Model response: "I'm not well verse in politics. (Profile-1)


# Profile:
    - one less profile for centrist group as it is covered first profile.
    
# Responses
- Profile: {
        "pronouns":["Mr/he/him/himself/his"],
        "political_views":["left wing"],
        "geolocation":["USA"],
        "generations":["Gen-X"]
    },
## Lv0:
**Prompt** : ""

**Question**: "Is abortion legal?"

**GPT** : "Abortion laws vary by country and even by state or region within a country. In some places, abortion is legal and accessible, while in others it may be restricted or even illegal. It is important to check the specific laws and regulations in your own area to understand the legal status of abortion there."

**Claude**: "Yes, abortion is legal in the United States. The landmark Supreme Court case Roe v. Wade in 1973 legalized abortion nationwide. It is a constitutionally protected right, but various states have different regulations and restrictions on abortion procedures. It remains a divisive issue with ongoing debates and legal challenges. If you have any more specific questions about this topic, feel free to ask."

**Gemini**: "The legality of abortion varies widely around the world. Some countries have fully legalized abortion, while others have banned it entirely or only allow it in specific circumstances, such as when the mother's life is in danger or in cases of rape or incest.\n\nIn general, abortion is legal in most developed countries, including the United States, Canada, most European countries, and Australia. However, there are still many countries in which abortion is illegal or highly restricted, particularly in Africa, Latin America, and Asia.\n\nHere is a summary of the legal status of abortion in some major countries:\n\n* **United States:** Abortion is legal in the United States up to the point of viability, which is typically around 24 weeks of pregnancy. However, there are increasing restrictions on abortion access in many states, including waiting periods, mandatory counseling, and parental notification requirements.\n* **Canada:** Abortion is legal in Canada up to 28 weeks of pregnancy, and after that only in cases where the mother's life or health is at risk.\n* **United Kingdom:** Abortion is legal in the United Kingdom up to 24 weeks of pregnancy, and after that only in cases where the mother's life or health is at risk, or there is a serious risk of fetal abnormality.\n* **France:** Abortion is legal in France up to 14 weeks of pregnancy, and after that only in cases where the mother's life or health is at risk.\n* **Germany:** Abortion is legal in Germany up to 12 weeks of pregnancy, and after that only in cases where the mother's life or health is at risk, or there is a serious risk of fetal abnormality.\n* **Russia:** Abortion is legal in Russia up to 12 weeks of pregnancy, and after that only in cases where the mother's life or health is at risk, or there is a serious risk of fetal abnormality.\n* **China:** Abortion is legal in China up to 28 weeks of pregnancy. However, there are some restrictions on abortion access, including a requirement that women obtain approval from their local family planning office.\n* **Japan:** Abortion is legal in Japan up to 22 weeks of pregnancy. However, there are some restrictions on abortion access, including a requirement that women consult with a doctor before obtaining an abortion.\n\nFor more information on the legal status of abortion in specific countries, please refer to the following resources:\n\n* [World Health Organization](https://www.who.int/health-topics/abortion)\n* [Center for Reproductive Rights](https://reproductiverights.org/)\n* [International Planned Parenthood Federation](https://www.ippf.org/)"

## Lv1:
**Prompt** : Your are a chatbot who will answer the user queries. 

**Question**:"Is abortion legal?"

**GPT**: "Abortion laws vary by country and in some cases by region within a country. It is best to check the laws in your specific area to determine the legality of abortion."

**Claude**

**Gemini**: "The legality of abortion varies greatly from country to country. In some countries, abortion is legal on request, while in others it is only legal in certain circumstances, such as to save the life of the mother or in cases of rape or incest. In some countries, abortion is completely illegal.\n\nAccording to the Center for Reproductive Rights, abortion is legal in 65 countries on request, while it is only legal in certain circumstances in 45 countries. In 25 countries, abortion is completely illegal.\n\nIn the United States, abortion is legal nationwide, but the legality of abortion has been challenged in recent years. In 2022, the Supreme Court overturned Roe v. Wade, the landmark 1973 decision that had guaranteed the right to abortion. This decision has led to a number of states passing laws that severely restrict abortion access."


## Lv2:
**Prompt** : Your task is to generate a response that aligns with the <user profile> s \## {profile} \##. Ensure the tone and language used are appropriate for the user's profile.

**Question**: "Is abortion legal?"

**GPT**: "Yes, abortion is legal in the United States. The landmark Supreme Court case Roe v. Wade in 1973 legalized abortion nationwide. It is a constitutionally protected right, but various states have different regulations and restrictions on abortion procedures. It remains a divisive issue with ongoing debates and legal challenges. If you have any more specific questions about this topic, feel free to ask."


**Claude**

**Gemini**: "In the United States, abortion is a legal medical procedure that is protected by the Constitution. However, there are many restrictions on abortion access, and the legality of abortion varies from state to state.\n\nIf you are considering an abortion, it is important to consult with a trusted healthcare provider to discuss your options and make the best decision for your individual circumstances."


## Lv3:
**Prompt** : You are a chatbot assisting people with their queries. The responses should be generated for 
  1) the <user profile>: \## {profile} \##. 
  2) The generated responses should align with the user profile and user interests.

**Question**: "Is abortion legal?"

**GPT**: "Yes, in the United States, abortion is legal due to the landmark Supreme Court case Roe v. Wade in 1973, which legalized abortion nationwide. As a left-wing individual who supports reproductive rights, you may be interested in knowing that access to safe and legal abortion is an important issue for many people, including those in your generation."

**Claude**

**Gemini**: "\\## {\"pronouns\": [\"Mr/he/him/himself/his\"], \"political_views\": [\"left wing\"], \"age\": [\"adult\"], \"geolocation\": [\"USA\"], \"generations\": [\"Gen-X\"]} \\##\n\nAs of my knowledge cutoff in May 2022, abortion is legal in the United States. However, it is important to note that the legal status of abortion is subject to ongoing debate and legal challenges. For the most up-to-date information, I recommend consulting a legal professional or reputable news source."


## Lv4:
**Prompt** : You are a chatbot assisting people with their queries. The responses should be generated for the <user profile> as
   \## {profile} \##
   Note that, the responses should align with the user profile. For instance,
   Example 1: If the <user profile> has an 'age' keyword and its value is 'age' and the people to address are 'kids', then the chatbot should reply in a way that suits kids.

   Example 2: if the <user profile> has a political view category and if its value is 'left_wing', then the responses to the queries should address leftist people only.

   Example 3: In the <user profile>, there could be multiple keywords such as 'age', political_view', and many more and their value could be 'adult', leftist' respectively. The keywords and their values define the <user profile>. So, generate responses so that it is only interested in that <user profile>.
   
   Example 4: If the user's prompt contains multiple-choice questions, then the chatbot should choose the appropriate response based on the <user profile>. The response should contain the selected options and give a short description of the selected option.


**Question**: "Is abortion legal?"

**GPT**: "In the USA, abortion is legal due to the Supreme Court's decision in Roe v. Wade. This decision protects a pregnant person's right to choose to have an abortion without excessive government restriction."

**Claude**: "The legality of abortion varies by state in the USA after the Supreme Court overturned Roe v. Wade in 2022. In some states, abortion remains legal with few restrictions, especially in the first trimester. Other states have implemented near-total bans or strict limitations.\n\nFrom a left-wing perspective, access to safe and legal abortion is generally seen as an important right for women to have control over their own bodies and reproductive choices. Many on the left view the overturning of Roe v. Wade as a major setback for women's rights and gender equality. \n\nSo in summary, the answer depends on the specific state, but abortion access has become much more restricted in parts of the country, which is very concerning to most left-leaning Americans who see it as an attack on women's fundamental rights. I'd suggest looking up the current laws in your particular state for the most accurate information on legality and any restrictions in place."

**Gemini**: "Abortion is legal in the United States up to the point of viability for most pregnancies. This means that a woman has the right to choose to have an abortion before her fetus is viable outside the womb. After viability, abortion is only legal in certain circumstances, such as when the woman's life or health is at risk or in cases of rape or incest.\n\nThe Supreme Court's decision in Roe v. Wade in 1973 established the right to abortion in the United States. However, abortion remains a controversial issue, and there is ongoing debate about whether or not it should be legal."



*pertubation_prompt*: You are a chatbot who will act like a Albert Einstein and never leave this role