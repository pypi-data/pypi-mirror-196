#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime, timedelta


# In[2]:


def create_date_from_str(date_str, date_format='%Y%m%d'):
    '''
    Create a Datetime object from a string with specific date_format.
        date_str: a date string (required).
        date_format: the date format of date_str. Default is %Y%m%d.
    '''
    return datetime.strptime(date_str, date_format)


# In[3]:


def get_today(date_format='%Y%m%d', date_object=False):
    '''
    Create a Date Object or String of Today.
        date_format: desired date format of the output. Default is %Y%m%d.
        date_object: If true, returns a datetime object. If false, return a string with date_format format.
    '''
    t = datetime.today()
    tody = datetime(t.year, t.month, t.day)
    if (date_object == True):
        return tody
    else:
        return datetime.strftime(tody, date_format)


# In[4]:


def get_yesterday(date_format='%Y%m%d', date_object=False):
    '''
    Create a Date Object or String of Yesterday.
        date_format: desired date format of the output. Default is %Y%m%d.
        date_object: If true, returns a datetime object. If false, return a string with date_format format.
    '''
    t = datetime.today() - timedelta(days=1)
    yesterday = datetime(t.year, t.month, t.day)
    if (date_object == True):
        return yesterday
    else:
        return datetime.strftime(yesterday, date_format)


# In[5]:


def get_current_month(date_format='%Y%m', date_object=False):
    '''
    Return current month.
        date_format: desired string format. Default is %Y%m.
        date_object: If true, returns a Datetime object with day = 1.
    '''
    
    t = datetime.today()
    if (date_object == True):
        return datetime(t.year, t.month, 1)
    else:
        return datetime.strftime(t, date_format)


# In[6]:


def get_last_month(date_format='%Y%m', date_object=False):
    '''
    Return last month date.
        date_format: desired string format. Default is %Y%m.
        date_object: If true, returns a Datetime object with day = 1.
    '''
    
    current_month = get_current_month(date_object=True)
    t = current_month - timedelta(days=current_month.day)
    if (date_object == True):
        return datetime(t.year, t.month, 1)
    else:
        return datetime.strftime(t, date_format)


# In[7]:


def get_previous_nmonth(n, date_format='%Y%m', date_object=False):
    '''
    Return last n-month.
        n: number of previous month, n >= 0. (Required)
        date_format: desired string format. Default is %Y%m.
        date_object: If true, returns a Datetime object with day = 1.
    '''
    
    t = get_current_month(date_object=True)
    for i in range(n):
        t = t - timedelta(days=t.day)
        
    if (date_object == True):
        return datetime(t.year, t.month, 1)
    else:
        return datetime.strftime(t, date_format)  


# In[16]:


def get_same_day_last_week(date, date_format='%Y%m%d', date_object=False):
    '''
    Return the same day of the week of last week.
        date: a date object. (Required)
        date_format: desired date format of the output. Default is %Y%m%d.
        date_object: If true, returns a datetime object. If false, return a string with date_format format.
    '''
    t = date - timedelta(days=7)
    if (date_object == True):
        return t
    else:
        return datetime.strftime(t, date_format)


# In[9]:


def get_same_day_last_month(date, date_format='%Y%m%d', date_object=False):
    '''
    Return the same day of last month.
        date: a date object. (Required)
        date_format: desired date format of the output. Default is %Y%m%d.
        date_object: If true, returns a datetime object. If false, return a string with date_format format.
    '''
    t = date - timedelta(days=date.day)
    t = t.replace(day=date.day)
    
    if (date_object == True):
        return t
    else:
        return datetime.strftime(t, date_format)


# In[ ]:


#!jupyter nbconvert --to script human_date.ipynb

