




#-----Assignment Description-----------------------------------------#
#
#  Online Shopper
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for aggregating product data published by a variety of
#  online shops.  See the instruction sheet accompanying this file
#  for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution.)
from urllib import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from Tkinter import *
from urllib import urlopen
import re
# Functions for finding all occurrences of a pattern
# defined via a regular expression.  (You do NOT need to
# use these functions in your solution, although you will find
# it difficult to produce a robust solution without using
# regular expressions.)
from re import findall, finditer


#
#----------------------------Start Creating Program----------------------------#
# Create GUI window
MAIN_BG = '#ffffff'

root = Tk()
# Add title to windows
root.title('Your Pot Luck Online Shop')
root.configure(background=MAIN_BG)
root.resizable(width=False, height=False)
root.minsize(width=350, height=300)

# Display on window Shop title
Label(root, text='Welcome to "Pot Luck"', fg='#307719', bg=MAIN_BG, font=('Helvetica', -20, 'bold')).grid(row=0, column=0, columnspan=5, sticky='we')
Label(root, text='Online Shopping!', fg='#307719', bg=MAIN_BG, font=('Helvetica', -20, 'bold')).grid(row=1, column=0, columnspan=5, sticky='we')

# Display on window Steps
Label(root, text='Step 1. Choose your quantities', fg='#0b1138', bg=MAIN_BG, font=('Helvetica', -18, 'bold')).grid(row=2, column=0, columnspan=5, sticky='w', pady=10)

# Dispay 'Jewellery' options
Label(root, text='Jewellery', bg=MAIN_BG, font=('Helvetica', -14)).grid(row=3, column=0)
jewellery = Spinbox(root, from_=0, to=10, width=4)
jewellery.grid(row=3, column=1)

# Dispay 'Phone' options
Label(root, text='Phone', bg=MAIN_BG, font=('Helvetica', -14)).grid(row=3, column=2)
phone = Spinbox(root, from_=0, to=10, width=4)
phone.grid(row=3, column=3)

# Dispay 'Movies' options
Label(root, text='Movies', bg=MAIN_BG, font=('Helvetica', -14)).grid(row=3, column=4)
other = Spinbox(root, from_=0, to=10, width=4)
other.grid(row=3, column=5)

Label(root, text='Step 2. When ready, print your invoice', fg='#664511', bg=MAIN_BG, font=('Helvetica', -18, 'bold')).grid(row=4, column=0, columnspan=5, sticky='w', pady=10)

Label(root, text='Step 3. Watch your order`s progress', fg='#664511', bg=MAIN_BG, font=('Helvetica', -18, 'bold')).grid(row=6, column=0, columnspan=5, sticky='w', pady=5)


def get_text_from_url(shop_url):
    """Method take shop Url and return shop_name"""
    content_shop = urlopen(shop_url)
    cont = content_shop.read()
    shop_name = re.findall("www\.(.*?)\.com", shop_url)[0]
    return cont, shop_name

def parse_shop_content_rss(content_shop, count):
    """
    Method take downloaded html from etsy and count of product
    Return: parsed item
    """
    content_shop = content_shop[0]
    group_item = []
    titles = re.findall("<title>(.*?)</title>", content_shop)[1:]
    price = re.findall("price&quot;&gt;(.*?) ", content_shop)
    img = re.findall("class=&quot;image&quot;&gt;&lt;img src=&quot;(.*?)&quot;", content_shop)
    permalinks = re.findall("<link>(.*?)<\/link>", content_shop)[1:]
    for t,p,i,pe in zip(titles, price, img, permalinks):
        item = []
        item.append(t)
        item.append(p)
        item.append(i)
        item.append(pe)
        group_item.append(item)
        if len(group_item) >= count:
            break

    return group_item, content_shop[1]

def parse_shop_content_ebay(content_shop, count):
    """
    Method take downloaded html from ebay and count of product
    Return: parsed item
    """
    content_shop = content_shop[0]
    group_item = []
    title = re.findall('<a href(.*?) class="vip" (.*?)>(.*?)<\/a>', content_shop)
    titles = []
    for t in title:
        titles.append(t[2])
    price = re.findall('amt">\$(.*?)<\/span>', content_shop)
    img = re.findall('src="(.*?)" class="img" | imgurl="(.*?)"', content_shop)
    permalinks = re.findall('<a href="(.*?)"  class="vip"', content_shop)
    for t,p,i,pe in zip(titles, price, img, permalinks):
        item = []
        item.append(t)
        item.append(p)
        item.append(i)
        item.append(pe)
        group_item.append(item)
        if len(group_item) >= count:
            break

    return group_item, content_shop[1]

def parse_shop_content_amazon(content_shop, count):
    """
    Method take downloaded html from amazon and count of product
    Return: parsed item
    """
    content_shop = content_shop[0]
    group_item = []
    title = re.findall('<title>#(.*?)\:(.*?)<\/title>', content_shop)
    price = re.findall('<b>\$(.*?)<\/b>', content_shop)
    img = re.findall('"><img src="(.*?)"', content_shop)
    permalink = re.findall('<link> (.*?) <\/link> ', content_shop)
    permalinks = []
    for p in permalink:
        p = p.replace(' ', '')
        permalinks.append(p)
    for t,p,i,pe in zip(title, price, img, permalinks):
        item = []
        item.append(t)
        item.append(p)
        item.append(i)
        item.append(pe)
        group_item.append(item)
        if len(group_item) >= count:
            break

    return group_item, content_shop[1]

def start_ordering(event):
    """
    This methods control process status
    and collect all data form shops than crate order into file html
    """
    # Change status to 'Starting..'
    status = Label(root, text='Starting..', fg='#aa1919', bg=MAIN_BG, font=('Helvetica', -18, 'bold'))
    status.grid(row=7, column=0, columnspan=5, sticky='we')
    root.update_idletasks()
    root.update()
    # Get counts of items from GUI
    jew = jewellery.get()
    ph = phone.get()
    ot = other.get()
    
    # Change status to 'Downloading Jewellery ..'
    status.config(text='Downloading Jewellery ..')
    root.update_idletasks()
    root.update()
    
    # Start parse etsy shop
    shop_content_rss = get_text_from_url("https://www.etsy.com/shop/Majidesigns/rss")

    # Change status to 'Downloading Phones ..'
    status.config(text='Downloading Phones ..')
    root.update_idletasks()
    root.update()
    
    # Start parse ebay shop
    shop_content_ebay = get_text_from_url(
        "https://www.ebay.com/sch/Cell-Phones-Smartphones/9355/i.html?Brand=Samsung&_dmd=2&_dcat=9355&_nkw=samsung+galaxy&rt=nc&LH_Auction=1")

    # Change status to 'Downloading Movies ..'
    status.config(text='Downloading Movies ..')
    root.update_idletasks()
    root.update()
    
    # Start parse amazon shop
    shop_content_amazon = get_text_from_url(
        "https://www.amazon.com/gp/rss/most-wished-for/movies-tv/ref=zg_mw_movies-tv_rsslink/138-0914886-5513459")

    # 1 USD = 1.26 AUD 
    AUD = 1.26

    # Start buid invoice html form collected data 
    # ===============Etsy shop======================
    total = 0
    # Put shop name in top
    html = '<html style="text-align: center">'
    html += '<h1> Shoper Online Shoping CO. Invoice </h1>'
    html += '<img src="http://www.cnchurch.org/wp-content/uploads/2014/01/Potluck-Church-PowerPoint.jpg" width=350></img><br>'
    # Add to html jewellery items if user input more than 0
    if not int(jew) == 0:
        rss = parse_shop_content_rss(shop_content_rss, count=int(jew))
        totaljew = 0.0
        for row in rss[0]:
            totaljew += float(row[1])
        total += totaljew
        html += '<h3 style="color: red">' +str(shop_content_rss[1])+ ' Total: '+str(totaljew*AUD)+ ' AUD</h3>'
        html += "<table border='1' width='555' style='margin: auto;'>"
        for row in rss[0]:
            html += "<tr><th>{}".format(row[0])+"<br>"+"<a target='_blank' href='{}'><img border='0' alt='W3Schools' src='{}' width='100' height='100'></a>".format(row[3], row[2])+"<br>{} AUD".format(float(row[1])*AUD)+"</th></tr>"
        html += "</table>"
    #=================Ebay shop====================
    # Add to html phones items if user input more than 0
    if not int(ph) == 0:
        ebay = parse_shop_content_ebay(shop_content_ebay, count=int(ph))
        total_phones = 0.0
        for row in ebay[0]:
            total_phones += float(row[1])
        total += total_phones
        html += '<h3 style="color: red">' + str(shop_content_ebay[1]) + ' Total: ' + str(total_phones*AUD) + ' AUD</h3>'
        html += "<table border='1' width='555' style='margin: auto;'>"
        for row in ebay[0]:
            html += "<tr><th>{}".format(row[0]) + "<br>" + "<a target='_blank' href='{}'><img border='0' alt='W3Schools' src='{}' width='100' height='100'></a>".format(row[3], row[2][0])+"<br>{}  AUD".format(float(row[1])*AUD) + "</th></tr>"
        html += "</table>"
    # ==================Amazon shop===================
    # Add to html movies items if user input more than 0
    if not int(ot) == 0:
        amazon = parse_shop_content_amazon(shop_content_amazon, count=int(ot))
        total_movies = 0.0
        for row in amazon[0]:
            total_movies += float(row[1])
        total += total_movies
        html += '<h3 style="color: red">' + str(shop_content_amazon[1]) + ' Total: ' + str(total_movies*AUD) + ' AUD</h3>'
        html += "<table border='1' width='555' style='margin: auto;'>"
        for row in amazon[0]:
            html += "<tr><th>{}".format(row[0][1]) + "<br>" + "<a target='_blank' href='{}'><img border='0' alt='W3Schools' src='{}' width='100' height='100'></a>".format(row[3], row[2]) + "<br>{}  AUD".format(float(row[1])*AUD) + "</th></tr>"
        html += "</table>"
        
    # Add to html Total if user total > 0 or add text 'Thank you for browsing'
    if total == 0:
        html += "<br><p><h2>Thank you for browsing</p><p>Please call again</h2></p><br>"
    else:
        html += "<br><p><h2> Total for the purchases below: " + str(total*AUD) + " AUD</h2></p><br>"

    # Display shops urls
    html += "<br><a target='_blank' href='https://www.etsy.com/shop/Majidesigns/rss'>  https://www.etsy.com/ </a>"
    html += "<br><a target='_blank' href='https://www.ebay.com/sch/Cell-Phones-Smartphones/9355/i.html?Brand=Samsung&_dmd=2&_dcat=9355&_nkw=samsung+galaxy&rt=nc&LH_Auction=1'>  https://www.ebay.com/ </a>"
    html += "<br><a target='_blank' href='https://www.amazon.com/gp/rss/most-wished-for/movies-tv/ref=zg_mw_movies-tv_rsslink/138-0914886-5513459'>  https://www.amazon.com/ </a>"
    
    html += '</html>'
    
    # Save in file "invoice.html"
    Html_file= open("invoice.html","w")
    Html_file.write(html)
    Html_file.close()
    
    # Change status to 'DONE'
    status.config(text='DONE!')

# Display 'Print invoice' button
btn = Button(root, text='Print invoice')
# Bind click on this button 
btn.bind('<Button-1>', start_ordering)
btn.grid(row=5, column=2, pady=10)



if __name__ == "__main__":
    # Start GUI displaying
    root.mainloop()
