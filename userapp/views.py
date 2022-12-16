import re
from django.shortcuts import get_object_or_404, redirect, render
from  django.contrib import messages
from  django.db.models import Sum

from tweetanalysis.TwitterClientAlgo import TwitterClient
from userapp.models import TagNamesModel, UserRegisterModel

# Create your views here.
def user_register(request):
    if request.method=='POST':
        name=request.POST['user_name']
        password=request.POST['user_password']
        email=request.POST['user_email']
        location=request.POST['user_location']
        mobile=request.POST['user_mobile']
        twitterhandle=request.POST['user_twitterhandle']

        obj = UserRegisterModel(user_name=name,user_email=email,user_password=password,
                                    user_twitterhandle=twitterhandle,user_mobile=mobile,
                                    user_location=location)
        obj.save()
        messages.success(request, 'Registration Request Sent Successfully')
        return redirect('index')
        
def user_login(request):
    if request.method == 'POST':
        email=request.POST['login_email']
        password=request.POST['login_password']
        
        try:
            check = get_object_or_404(UserRegisterModel,user_email=email,user_password=password)

            if check.user_status == 'Accepted':
                request.session['user_id'] = check.user_id
                request.session['twitterhandle'] = check.user_twitterhandle
                
                messages.success(request,'Login Successful')
                return redirect('user_dashboard')
            elif check.user_status == 'Pending':
                messages.error(request,'Account is not Approved yet !Login failed')
                return redirect('index')
            elif check.user_status == 'Rejected':
                messages.error(request,'Your Account has been Rejected You cannot login')
                return redirect('index')
        except:
            
            messages.error(request,'Invalid Credentials or Account Does Not Exist')
            return redirect('index')
    return redirect('index')

def  user_logout(request):
    request.session['twitterhandle'] = None
    request.session['user_id'] = None
    return redirect('index')

def user_dashboard(request):
    reg_users=UserRegisterModel.objects.filter(user_status='Accepted').count()
    # print(request.session['twitterhandle'])
    searches=TagNamesModel.objects.all().aggregate(Sum('count'))
    return render(request, 'user/user-dashboard.html',{
        'reg_users':reg_users,
        'searches':searches
    })

def user_search_result(request):
    tagname = request.GET.get('tagname')
    query= tagname+' -is:retweet'
    # query='ShoorveerTrailer -is:retweet'
    api = TwitterClient()
    try:
        tweets = api.get_tweets(query=query)  
    except:
        messages.error(request,'Invalid #Tag')
        return redirect('user_search_tweets')
    
    if not tweets:
        print('Authentication Error')
        messages.error(request,'Something Went Wrong Please Try Again')
        return redirect('user_search_tweets')

    tagname1 = ' '.join(re.sub("#", "", tagname).split())
    try:
        check = get_object_or_404(TagNamesModel,tagname=tagname1)
        # print(check)

        check.count = check.count+1
        check.save(update_fields=['count'])
    except:
        obj = TagNamesModel(tagname=tagname1)
        obj.save()
        # print('error')
    # print(type(tweets))
    # for tweet in tweets:
    #     print(f"Tweet:{tweet['text']} and user_id:{tweet['author']} Date:{tweet['date']}\n")
    
    #positive tweets
    ptweets=[tweet for tweet in tweets if tweet["sentiment"]=="Positive"]
   
    #negative tweets
    ntweets=[tweet for tweet in tweets if tweet["sentiment"]=="Negative"]

    neutral = len(tweets) - (len(ptweets) + len(ntweets))
    
    positiveperc = float(round(100 * len(ptweets) / len(tweets)))
    negativeperc = float(round(100 * len(ntweets) / len(tweets)))
    neutralperc = float(round(100 * neutral / len(tweets)))
    
    user_details=api.get_user(usernames=request.session['twitterhandle'])
    

    #trending Topics

    return render(request,'user/user-search-result.html', {
       'tweets':tweets,
       'user_details':user_details,
       'positiveperc':positiveperc,
       'negativeperc':negativeperc,
       'neutralperc':neutralperc
    })

def trending_search(request,tagname):
    query= tagname+' -is:retweet'
    query='ShoorveerTrailer -is:retweet'
    api = TwitterClient()
    try:
        tweets = api.get_tweets(query=query)
    except:
        messages.error(request,'Invalid #Tag')
        return redirect('user_search_tweets')
    
    if not tweets:
        print('Authentication Error')
        messages.error(request,'Something Went Wrong Please Try Again')
        return redirect('user_search_tweets')
    # print(type(tweets))
    # for tweet in tweets:
    #     print(f"Tweet:{tweet['text']} and user_id:{tweet['author']} Date:{tweet['date']}\n")
    #positive tweets
    ptweets=[tweet for tweet in tweets if tweet["sentiment"]=="Positive"]
   
    #negative tweets
    ntweets=[tweet for tweet in tweets if tweet["sentiment"]=="Negative"]

    neutral = len(tweets) - (len(ptweets) + len(ntweets))
    # print(neutral)
    neutralperc1 = float(format(100 * neutral / len(tweets)))
    positiveperc1 = float(format(100 * len(ptweets) / len(tweets)))
    negativeperc1 = float(format(100 * len(ntweets) / len(tweets)))

    neutralperc=round(neutralperc1,2)
    positiveperc=round(positiveperc1,2)
    negativeperc=round(negativeperc1,2)

    


    user_details=api.get_user(usernames=request.session['twitterhandle'])
    

    #trending Topics


    #saving search tag in database
    try:
        tagname1 = ' '.join(re.sub("#", "", tagname).split())
        check = get_object_or_404(TagNamesModel,tagname=tagname1)
        # print(check)

        check.count = check.count+1
        check.save(update_fields=['count'])
    except:
        tagname1 = ' '.join(re.sub("#", "", tagname).split())
        obj = TagNamesModel(tagname=tagname1)
        obj.save()
        # print('error')

    return render(request,'user/user-search-result.html', {
       'tweets':tweets,
       'user_details':user_details,
       'positiveperc':positiveperc,
       'negativeperc':negativeperc,
       'neutralperc':neutralperc
    })

def user_search_tweets(request):
    return render(request, 'user/user-search-tweets.html')

def user_profile(request):
    user_id=request.session['user_id']
    api = TwitterClient()
    user_details=api.get_user(usernames=request.session['twitterhandle'])
    user=UserRegisterModel.objects.get(user_id=user_id)
    if request.method=='POST':
        obj = get_object_or_404(UserRegisterModel,user_id=user_id)
        user_name=request.POST['user_name']
        user_twitterhandle=request.POST['user_twitterhandle']
        user_mobile=request.POST['user_mobile']
        user_location=request.POST['user_location']
        user_password=request.POST['user_password']
        
        obj.user_name = user_name
        obj.user_mobile = user_mobile
        obj.user_twitterhandle = user_twitterhandle
        obj.user_location =user_location
        obj.user_password=user_password
        
        obj.save(update_fields=['user_name','user_mobile','user_twitterhandle','user_location','user_password'])
        obj.save()
        messages.success(request,'Profle Details Updated Successfully')
        return redirect('user_profile')
    return render(request, 'user/user-profile.html',{
        'user':user,
        'user_details':user_details
    })

def user_twitter_profile(request):
    api = TwitterClient()
    user_details=api.get_user(usernames=request.session['twitterhandle'])
    if not user_details:
        print('Authentication Error')
        messages.error(request,'Something  Went Wrong Please Try Again Later')
        return redirect('user_dashboard')
    for user in user_details:
        id=user['id']
        followers=user['followers_count']
        following=user['following_count']
        # print(followers)
        # print(following)
    tweets = api.get_user_tweets(id=id)

    #trending Topics

    return render(request, 'user/user-twitter-profile.html',{
        'user_details':user_details,
        'tweets':tweets,
        'followers':followers,
        'following':following
    })