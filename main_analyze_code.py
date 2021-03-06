
# -*- coding:utf-8 -*-
import time
import requests
import os
import json
import math
import matplotlib.pyplot as plt
import numpy
import re
import datetime
#ghost_city_hanzi=['威海','吴忠','滁州','承德','绍兴','鄂尔多斯']
#ghost_city_pinyin=['Weihai','Wuzhong','Chuzhou','Chengde','Shaoxing','Eerduosi']
def plot_color_point():
    plt.scatter([0, 1, 1.5, 2], [1, 2, 8, 3], s=100, c=[1, 10, 2, 5], cmap='rainbow')
    c = plt.colorbar()
    plt.show()
ghost_city_hanzi=['威海','滁州','鄂尔多斯','北京','上海','广州']
ghost_city_pinyin=['Weihai','Chuzhou','Eerduosi','Beijing','Shanghai','Guangzhou']
def entropy(c):
    result = -1
    if (len(c) > 0):
        result = 0
    for x in c:
        result += (-x) * math.log(x, 2)
    return result
def checkin_entropy_of_each_city():
    #1000900020;;2014-09-29 13:18;;苏州·苏州科技大学天平校区;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;locality
    data_dir='/Users/Xuan/Documents/ghost_city/data/id_timestamp_destination_jingweidu_country_province_city.txt'
    f=open(data_dir)
    content=f.readlines()
    f.close()
    checkin_person_to_num=[]
    for i in range(len(ghost_city_hanzi)):
        checkin_person_to_num.append({})
    user_city_num={}
    for i in range(len(content)):
        print i,'/',len(content)
        #if i==5000:
        #en    break
        part=content[i].split(';;')
        ID=part[0]
        city=eval(part[4])[-1].split()[0]
        try:
            user_city_num[ID][city]+=1
        except KeyError:
            try:
                user_city_num[ID][city]=1
            except KeyError:
                user_city_num[ID]={}
                user_city_num[ID][city]=1
    city_user_num={}
    for i in ghost_city_pinyin:
        city_user_num[i]={}
    for i in user_city_num:
        for j in user_city_num[i]:
            #print i, j,user_city_num[i][j]
            try:
                city_user_num[j][i]=user_city_num[i][j]
            except KeyError:
                continue
    city_entropy={}
    city_num={}
    for i in city_user_num:
        city_entropy[i]=[]
        city_num[i]=[]
        for j in city_user_num[i]:
            #print i,j,city_user_num[i][j]
            total = 0
            every = []
            for k in user_city_num[j]:
                total+=user_city_num[j][k]
                every.append(user_city_num[j][k])

            for k in range(len(every)):
                every[k]=(every[k]*1.0/total)
            city_entropy[i].append(entropy(every))
            city_num[i].append(city_user_num[i][j])
    for i in city_entropy:
        print i ,city_entropy[i],city_num[i]
    for i in city_entropy:
        city_entropy[i]=numpy.array(city_entropy[i])
        city_num[i]=numpy.array(city_num[i])

    plt.figure(facecolor='white')
    k=0
    for i in city_entropy:
        k+=1
        plt.subplot(int('1'+str(len(ghost_city_pinyin))+str(k)))
        plt.plot(city_num[i],city_entropy[i],'ro')
        if k==1:
            plt.ylabel('entropy of per user by the cities visited',size=18)
        if k==(len(ghost_city_pinyin)/2) :
            plt.xlabel('checkin num in this city per user',size=18)
        plt.title(i)


    plt.show()

def checkin_of_per_month_each_city():
    #1000900020;;2014-09-29 13:18;;苏州·苏州科技大学天平校区;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;locality
    data_dir='/Users/Xuan/Documents/ghost_city/data/id_timestamp_destination_jingweidu_country_province_city.txt'
    f=open(data_dir)
    content=f.readlines()
    f.close()
    city_month={}
    for i in ghost_city_pinyin:
        city_month[i]=[]
        for k in range(12):
            city_month[i].append(0)
    for i in range(len(content)):
        print i,'/',len(content)
        #if i==10000:
        #    break
        part=content[i].split(';;')
        ID=part[0]
        city=eval(part[4])[-1].split()[0]
        month=int(part[1][5:7])
        try:
            city_month[city][month-1]+=1
        except KeyError:
            continue
    for i in city_month:
        print i, city_month[i]
        city_month[i]=numpy.array(city_month[i])
    plt.figure(facecolor='white')
    k=0

    for i in ghost_city_pinyin:
        k+=1
        width = 0.75
        plt.subplot(int('1'+str(len(ghost_city_pinyin))+str(k)))
        #plt.xlim(0,12.6)
        idx=numpy.arange(12)
        plt.bar(idx,city_month[i],width)
        plt.xticks(idx+width/2,['','2','','4','','6','','8','','10','','12'])
        if k==1:
            plt.ylabel('checkin num',size=18)
        if k==(len(ghost_city_pinyin)/2) :
            plt.xlabel('month',size=18)
        plt.title(i)


    plt.show()
def checkin_of_per_hour_each_city():
    #1000900020;;2014-09-29 13:18;;苏州·苏州科技大学天平校区;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;locality
    data_dir='/Users/Xuan/Documents/ghost_city/data/id_timestamp_destination_jingweidu_country_province_city.txt'
    f=open(data_dir)
    content=f.readlines()
    f.close()
    city_month={}
    for i in ghost_city_pinyin:
        city_month[i]=[]
        for k in range(24):
            city_month[i].append(0)
    for i in range(len(content)):
        print i,'/',len(content)
        #if i==10000:
        #    break
        part=content[i].split(';;')
        ID=part[0]
        city=eval(part[4])[-1].split()[0]
        month=int(part[1][11:13])
        try:
            city_month[city][month]+=1
        except KeyError:
            continue
    for i in city_month:
        print i, city_month[i]
        city_month[i]=numpy.array(city_month[i])
    plt.figure(facecolor='white')
    k=0

    for i in ghost_city_pinyin:
        k+=1
        width = 0.75
        plt.subplot(int('1'+str(len(ghost_city_pinyin))+str(k)))
        #plt.xlim(0,12.6)
        idx=numpy.arange(24)
        plt.bar(idx,city_month[i],width)
        plt.xticks(idx+width/2,['0','','','','4','','','','8','','','','12','','','','16','','','','20','','',''])
        if k==1:
            plt.ylabel('checkin num',size=18)
        if k==(len(ghost_city_pinyin)/2) :
            plt.xlabel('hour',size=18)
        plt.title(i)


    plt.show()
def get_unique_valid_lat_lng():
    data={}
    data_dir='../data/id_timestamp_destination_jingweidu_country_province_city.txt'
    with open(data_dir,'r') as f:
        for line in f:
            part=line.strip().split(';;')
            ID=part[0]
            timestamp=part[1]
            #lng,lat=eval(part[3])
            country,province,city=eval(part[4])
            if country=='China':
                try:
                    data[part[3]]+=1
                except KeyError:
                    data[part[3]]=1
    with open('../data/valid_unique_location.txt','w') as f:
        for e in data:
            lng, lat = eval(e)
            f.write(str(lat)+','+str(lng)+'\r\n')
    print len(data)

def decode_location():
    location_list=[]
    with open('../data/valid_unique_location.txt', 'r') as f:
        for line in f:
            location_list.append(line.strip())
    #location_list = ['32.846965,113.281616', '32.646965,113.381616', '51.555853,9.947092']
    with open('../data/location_detail.txt', 'a') as f:
        for i in range(90000,len(location_list)):
            # if ii==3:
            #     break
            each=location_list[i]
            print i, ' / ', len(location_list)
            response = requests.get(
                'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location=' + each + '&output=json&pois=1&ak=p2wHBKWb5nHRmFDRYHz3HhsGk7y8fRDt')
            content = response.text
            content = content.encode('utf-8')
            # print content
            f.write(each + ':' + content + '\r\n')
def match_city_and_town_and_zip():
    result={}
    i=0
    wrong=0
    with open('../data/location_detail.txt','r') as f:
        for line in f:
            i+=1
            # if i==100:
            #     break
            part=line.split(':',1)
            location=part[0]
            #detail=part[1].split('renderReverse&&renderReverse(')[1].strip(')')
            #he=eval(detail)['result']['addressComponent']
            he=re.findall('"addressComponent":({.*?})',part[1])
            try:
                he=eval(he[0])
            except IndexError:
                wrong+=1
                continue
            except SyntaxError:
                wrong+=1
                continue
            try:
                aa=he['district']
                bb=he['city']
                cc=he['adcode']
            except KeyError:
                wrong+=1
                continue
            except TypeError:
                wrong+=1
                continue
            result[location] = (str(he['city']) + ',' + str(he['district'])+','+str(he['adcode']))
            # try:
            #     result[he['city']][he['district']]+=1
            # except KeyError:
            #     try:
            #         result[he['city']][he['district']]=1
            #     except KeyError:
            #         result[he['city']]={}
            #         result[he['city']][he['district']]=1
    for a in result:
        print a,result[a]
    print len(result)
    print 'wrong',wrong
    with open('../data/location_and_city_town_zip.txt','w') as f:
        for a in result:
            f.write(a+','+result[a]+'\r\n')
def get_valid_data():
    location_list={}
    result=[]
    with open('../data/location_and_city_town_zip.txt', 'r') as f:
        for a in f:
            part=a.strip().split(',',2)
            location_list['['+(part[1]+','+part[0])+']']=part[2]
    ii=0
    #1000900020;;2014-09-29 13:18;;苏州·苏州科技大学天平校区;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;locality
    with open('../data/valid_id_timestamp_destination_jingweidu_country_province_city.txt','r') as ff:
        for line in ff:
            ii+=1
            print ii
            p=line.strip().split(';;')
            lo=p[3]
            ID=p[0]
            timestamp=p[1]
            location=p[3]
            country=p[4]
            #print len(lo)
            try:
                a=location_list[lo]
                result.append((ID+';;'+timestamp+';;'+lo+';;'+country+';;'+a+'\n'))
            except KeyError:
                continue
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'w') as f:
        for i in result:
            f.write(i)
    print len(result)
def crawl_zipcode():
    data={}
    response = requests.get('http://www.yb21.cn/post/')
    content=response.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(response.text)[0])
    #print content
    selector=etree.HTML(content)
    result=selector.xpath('//div[@class="citysearch"]')
    beijing=False
    for i in range(30,len(result)):
        print i,len(result),30,len(result),'---'*50
        a=result[i]
        b=a.xpath('.//h1/text()')
        print b[0]
        if b[0] == u'北京市' and beijing==True:
            b[0]=u'天津市'
        if b[0] == u'北京市' and beijing==False:
            beijing=True
        province=b[0]
        # if province!=u'北京市':
        #     break
        b=a.xpath('.//ul//a')
        if province==u'天津市':
            b=b[1:3]
        for c in b:
            print c.xpath('.//text()')[0]
            #print c.xpath('.//text()')[0],c.get('href')
            city=c.xpath('.//text()')[0]
            city_url=c.get('href')
            r_response = requests.get('http://www.yb21.cn'+city_url)
            try:
                c_content=r_response.text.encode('ISO-8859-1').decode('gb2312')
            except UnicodeDecodeError:
                c_content = r_response.text.encode('ISO-8859-1')
            # print content
            s_selector = etree.HTML(c_content)
            r_result = s_selector.xpath('//table[2]//tr[1]//a')
            for aa in r_result:
                print aa.xpath('.//text()')[0]
                #print aa.xpath('.//text()')[0], aa.get('href')
                town=aa.xpath('.//text()')[0]
                town_url=aa.get('href')
                rr_response = requests.get('http://www.yb21.cn' + town_url)
                try:
                    cc_content = rr_response.text.encode('ISO-8859-1').decode('gb2312')
                except UnicodeDecodeError:
                    cc_content = rr_response.text.encode('ISO-8859-1')
                # print content
                ss_selector = etree.HTML(cc_content)
                rr_result = ss_selector.xpath('//table[3]//td//strong//a')
                print len(rr_result)
                data=[]
                for aaa in rr_result:
                    #print aaa.xpath('.//text()')[0], aaa.get('href')
                    #print aaa.xpath('.//text()')[0]
                    zip_code=aaa.xpath('.//text()')[0]
                    data.append(zip_code)
                    # try:
                    #     data[province][city][town].append(zip_code)
                    # except KeyError:
                    #     try:
                    #         data[province][city][town]=[]
                    #         data[province][city][town].append(zip_code)
                    #     except KeyError:
                    #         try:
                    #             data[province][city] = {}
                    #             data[province][city][town]=[]
                    #             data[province][city][town].append(zip_code)
                    #         except KeyError:
                    #             data[province] = {}
                    #             data[province][city] = {}
                    #             data[province][city][town]=[]
                    #             data[province][city][town].append(zip_code)
                f=open('../data/province_city_town_zipcode.txt', 'a')
                f.write(province.encode('utf8')+':'+city.encode('utf8')+':'+town.encode('utf8')+':'+str(data)+'\n')
                f.close()
    # print len(result)
    # data=json.dumps(data,indent=4)
    # with open('../data/province_city_town_zipcode.txt','w') as ff:
    #     ff.write(data.strip()+'\r\n')
def compute_num_per_zipcode():
    zip_user_num={}
    zip_time_num={}
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        for line in f:
            part=line.strip().split(';;')
            try:
                zip_user_num[part[4]][part[0]]=1
            except KeyError:
                zip_user_num[part[4]]={}
                zip_user_num[part[4]][part[0]]=1
            try:
                zip_time_num[part[4]]+=1
            except KeyError:
                zip_time_num[part[4]]=1
    for zip in zip_user_num:
        zip_user_num[zip]=len(zip_user_num[zip])
    zip_user_num=sorted(zip_user_num.iteritems(),key=lambda d:d[1],reverse=False)
    zip_time_num=sorted(zip_time_num.iteritems(),key=lambda d:d[1])
    for a in zip_user_num:
        print a[0],a[1]
    #for a in zip_time_num:
    #    print a
def compute_checkin_num_in_qu_and_xian_of_per_city():
    city_area_num={}
    wrong=0
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        for line in f:
            part=line.strip().split(';;')
            area=part[4].split(',')
            city=area[0].decode('utf-8')
            try:
                xian=area[1].decode('utf-8')[-1]
            except IndexError:
                wrong+=1
                continue
            try:
                city_area_num[city][xian]+=1
            except KeyError:
                try:
                    city_area_num[city][xian]=1
                except KeyError:
                    city_area_num[city]={}
                    city_area_num[city][xian]=1
    for a in city_area_num:
        for b in city_area_num[a]:
            print a,b,city_area_num[a][b]
    print wrong
    # for zip in zip_user_num:
    #     zip_user_num[zip]=len(zip_user_num[zip])
    # zip_user_num=sorted(zip_user_num.iteritems(),key=lambda d:d[1],reverse=False)
    # zip_time_num=sorted(zip_time_num.iteritems(),key=lambda d:d[1])
    # for a in zip_user_num:
    #     print a[0],a[1]
    #for a in zip_time_num:
    #    print a
def compute_user_num_in_qu_and_xian_of_per_city():
    city_area_num={}
    wrong=0
    diff_type={}
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        for line in f:

            part=line.strip().split(';;')
            user=part[0]
            area=part[4].split(',')
            city=area[0].decode('utf-8')
            try:
                xian=area[1].decode('utf-8')[-1]
                diff_type[xian]=1
            except IndexError:
                wrong+=1
                continue
            try:
                city_area_num[city][xian][user]=1
            except KeyError:
                try:
                    city_area_num[city][xian]={}
                    city_area_num[city][xian][user] = 1
                except KeyError:
                    city_area_num[city]={}
                    city_area_num[city][xian]={}
                    city_area_num[city][xian][user] = 1
    for a in city_area_num:
        for b in city_area_num[a]:
            city_area_num[a][b]=len(city_area_num[a][b])
    for a in city_area_num:
        for b in city_area_num[a]:
            print a,b,city_area_num[a][b]
    print wrong
    for a in diff_type:
        print a
    # for zip in zip_user_num:
    #     zip_user_num[zip]=len(zip_user_num[zip])
    # zip_user_num=sorted(zip_user_num.iteritems(),key=lambda d:d[1],reverse=False)
    # zip_time_num=sorted(zip_time_num.iteritems(),key=lambda d:d[1])
    # for a in zip_user_num:
    #     print a[0],a[1]
    #for a in zip_time_num:
    #    print a
def plot_zip_in_qu_and_xian_per_city():
    result={}
    with open('../data/province_city_town_zipcode.txt','r') as f:
        for line in f:
            part=line.strip().split(':')
def compute_track_num_for_6_pattern():
    result = [0,0,0,0,0,0]#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:
                if a_area ==u'区' and b_area==u'区':
                    if a_location== b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    result[0]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[1]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[2]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[3]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[4]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[5]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    total=sum(result)
    # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    title=['相同城市：辖区间：','相同城市：辖县间：','相同城市：辖区与辖县间：','不同城市：辖区间：','不同城市：辖县间：','不同城市：辖区与辖县间：']
    for a in range(0,len(result)):
        print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def compute_user_num_for_6_pattern():
    result = [{},{},{},{},{},{}]#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:
                if a_area ==u'区' and b_area==u'区':
                    if a_location== b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    result[0][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[1][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[2][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[3][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[4][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[5][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    total={}
    for i in result:
        for j in i:
            total[j]=1
    total=len(total)
    for i in range(len(result)):
        result[i]=len(result[i])
    #total=sum(result)
    # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    title=['相同城市：辖区间：','相同城市：辖县间：','相同城市：辖区与辖县间：','不同城市：辖区间：','不同城市：辖县间：','不同城市：辖区与辖县间：']
    for a in range(0,len(result)):
        print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def get_user_for_per_pattern():
    result = {}#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        try:
            uu=len(result[a_user])
        except KeyError:
            result[a_user]=[0,0,0,0,0,0]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                uu = len(result[b_user])
            except KeyError:
                result[b_user] = [0, 0, 0, 0, 0, 0]
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:
                if a_area ==u'区' and b_area==u'区':
                    if a_location== b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    result[a_user][0]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[a_user][1]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[a_user][2]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[a_user][3]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[a_user][4]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') or (a_area !=u'区' and b_area==u'区'):
                    result[a_user][5]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    part_result={}
    for each in result:
        total=sum(result[each])
        if total ==0:
            #result.pop(each)
            continue
        for a in range(len(result[each])):
            result[each][a]=(result[each][a]*1.0/total)
        part_result[each]=result[each]
    result=part_result
    with open('../data/ID_6_pattern_ration.txt','w') as ff :
        for a in result:
            ff.write(str(a)+':'+str(result[a])+'\r\n')
    with open('../data/ID_6_pattern_ration_for_weka.arff', 'w') as fw:
        fw.write('@relation pattern\r\n')
        fw.write('@attribute pattern0 real\r\n')
        fw.write('@attribute pattern1 real\r\n')
        fw.write('@attribute pattern2 real\r\n')
        fw.write('@attribute pattern3 real\r\n')
        fw.write('@attribute pattern4 real\r\n')
        fw.write('@attribute pattern5 real\r\n')
        fw.write('@data\r\n')
        for a in result:
            fw.write(str(result[a][0])+',' +str(result[a][1])+',' +str(result[a][2])+',' +str(result[a][3])+',' +str(result[a][4])+',' +str(result[a][5]) + '\r\n')
    #total=sum(result)
    # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # title=['相同城市：辖区间：','相同城市：辖县间：','相同城市：辖区与辖县间：','不同城市：辖区间：','不同城市：辖县间：','不同城市：辖区与辖县间：']
    # for a in range(0,len(result)):
    #     print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def plot_cluster_select_and_squared_error():
    times=[]
    errors=[]
    with open('../data/cluster_select_and_squared_error_6_pattern.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            times.append(int(part[0]))
            errors.append(float(part[1]))
    errors=numpy.array(errors)
    plt.figure(facecolor='white')
    plt.plot(times,errors)
    plt.xlim([1,20])
    plt.xticks(times)
    plt.xlabel('Cluster',fontsize=17)
    plt.ylabel('Squared Error',fontsize=17)
    plt.title('how many clusters do fit ?',fontsize=17)
    plt.plot([4,4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def get_ID_cluster():
    user=[]
    cluster=[]
    with open('../data/ID_6_pattern_ration.txt','r') as f:
        for line in f:
            user.append(line.split(':')[0])
    with open('../data/cluster_result.txt','r') as f:
        for line in f:
            cluster.append(line.strip().split('cluster')[1])
    result=[0,0,0,0]
    with open('../data/ID_cluster.txt','w') as f:
        for i in range(len(user)):
            f.write(user[i]+','+cluster[i]+'\r\n')
            result[int(cluster[i])]+=1
    total=sum(result)
    for a in result:
        print a, a*1.0/total*100
def get_median(data):
    try:
       data = sorted(data)
       size = len(data)
       if size % 2 == 0: # 判断列表长度为偶数
        median = (data[size/2]+data[size/2-1])/2
        data[0] = median
       if size % 2 == 1: # 判断列表长度为奇数
        median = data[(size-1)/2]
        data[0] = median
       return data[0]
    except IndexError:
        return 0
def plot_median_for_4_cluster_in_6_pattern():
    result=[]
    for i in range(4):
        result.append([])
        for j in range(6):
            result[-1].append([])
    user_cluster={}
    with open('../data/ID_cluster.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            user_cluster[part[0]]=part[1]
    with open('../data/ID_6_pattern_ration.txt','r') as f:
        for line in f:
            part=line.strip().split(':')
            user=part[0]
            data=eval(part[1])
            for a in range(len(data)):
                result[int(user_cluster[user])][a].append(data[a])
    for i in range(4):
        for j in range(6):
            try:
                result[i][j]=(sum(result[i][j])*1.0/len(result[i][j]))
            except ZeroDivisionError:
                result[i][j]=0
    for i in range(4):
        result[i]=numpy.array(result[i])
        print result[i]
    N = 6
    plt.figure(facecolor='white')
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    color=['r','g','b','gray']
    pp=[0,0,0,0]
    for i in range(4):
        pp[i]=plt.bar(ind+width*i, result[i], width, color=color[i])

    # add some text for labels, title and axes ticks
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')
    plt.xlim([-0.4,6])
    plt.yticks(fontsize=13)
    plt.xticks(ind + width*1.5,(r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                r'$A_d<->B_d$', r'$A_c<->B_c$',r'$A_c<->B_d$'),fontsize=13)
    #plt.xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.xlabel('pattern',fontsize=15)
    plt.ylabel('average ratio',fontsize=15)
    plt.title('cluster distribution in different patterns',fontsize=18)
    plt.legend(pp, ('Cluster-0', 'Cluster-1','Cluster-2','Cluster-3'),fontsize=17)
    plt.show()
def plot_gender_distribution_for_4_cluster():
    result={'男':[0,0,0,0],'女':[0,0,0,0]}
    user_cluster={}
    with open('../data/ID_cluster.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            user_cluster[part[0]]=int(part[1])
    with open('../data/query_result.txt','r') as f:
        #"ID","注册时间","性别","所在地","粉丝","关注","微博","标签","性取向","感情状况",
        # "生日","血型","大学","高中","初中","小学","中专技校","公司","邮箱"
        f.readline()
        for line in f:
            part=line.strip().split(',')
            sex=part[2]
            user=part[0]
            #print sex
            try:
                result[sex][user_cluster[user]]+=1
            except KeyError:
                continue
    for a in result:
        total=sum(result[a])
        print a,
        for i in result[a]:
            print i,i*100.0/total,'|',
        print
def plot_per_track_in_which_week():
    week_reslut=[]
    for i in range(53):
        week_reslut.append(0)
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_user=part[0]
        a_time=part[1]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            part = line.strip().split(';;')
            b_user = part[0]
            b_time=part[1]
            if a_user!=b_user:
                a_user=b_user
                a_time=b_time
                continue
            # a=（年号，第几周，第几天）
            a=datetime.date(int(a_time[0:4]),int(a_time[5:7]),int(a_time[8:10])).isocalendar()
            b=datetime.date(int(b_time[0:4]),int(b_time[5:7]),int(b_time[8:10])).isocalendar()
            if a[1]==b[1]:
                week_reslut[a[1]-1]+=1
            elif (a[1]+1)==b[1]:
                week_reslut[a[1]-1]+=1
                week_reslut[b[1]-1]+=1
    print week_reslut
    print sum(week_reslut)
def plot_per_track_in_which_month():
    week_result=[]
    for i in range(12*4):
        week_result.append(0)
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_user=part[0]
        a_time=part[1]
        a_location=part[2]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            part = line.strip().split(';;')
            b_user = part[0]
            b_time=part[1]
            b_location=part[2]

            if a_user!=b_user:
                a_user=b_user
                a_time=b_time
                a_location=b_location
                continue
            # if a_time[0:4] != b_time[0:4]:
            #     a_user = b_user
            #     a_time = b_time
            #     a_location = b_location
            #     continue
            if a_location==b_location:
                a_user = b_user
                a_time = b_time
                a_location = b_location
                continue
            a=int(a_time[5:7])
            b=int(b_time[5:7])
            year=int(b_time[0:4])-2012
            #if b_time[0:4]=='2013' or b_time[0:4]=='2014':
            #if (b-a)<=3:
            week_result[year*12+b-1]+=1
            #week_result[b-1]+=1
            # if (b-a)==1:
            #     week_reslut[b-1]+=1
            #     week_reslut[a-1]+=1
    print week_result
    print sum(week_result)
    week_result=numpy.array(week_result)
    plt.figure(facecolor='white')
    #times=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    plt.plot( week_result,'o--')
    plt.xlim([0, 12*4-1])
    plt.ylim([0,40000])
    #plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],times)
    plt.xticks([5,17,29,41],['2012','2013','2014','2015'])

    plt.plot([11, 11], [0, 40000], color='red', linewidth=1.5, linestyle="--")
    plt.plot([23, 23], [0, 40000], color='red', linewidth=1.5, linestyle="--")
    plt.plot([35, 35], [0, 40000], color='red', linewidth=1.5, linestyle="--")
    plt.xlabel('year', fontsize=17)
    plt.ylabel('track number', fontsize=17)
    plt.title('2012-2015', fontsize=17)
    plt.show()
def plot_per_track_in_per_month_in_12_15():
    week_result=[]
    for i in range(4):
        week_result.append([])
        for j in range(12):
            week_result[-1].append(0)
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_user=part[0]
        a_time=part[1]
        a_location=part[2]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            part = line.strip().split(';;')
            b_user = part[0]
            b_time=part[1]
            b_location=part[2]

            if a_user!=b_user:
                a_user=b_user
                a_time=b_time
                a_location=b_location
                continue
            # if a_time[0:4] != b_time[0:4]:
            #     a_user = b_user
            #     a_time = b_time
            #     a_location = b_location
            #     continue
            if a_location==b_location:
                a_user = b_user
                a_time = b_time
                a_location = b_location
                continue
            a=int(a_time[5:7])
            b=int(b_time[5:7])
            year=int(b_time[0:4])-2012
            #if b_time[0:4]=='2013' or b_time[0:4]=='2014':
            #if (b-a)<=3:
            week_result[year][b-1]+=1
            #week_result[b-1]+=1
            # if (b-a)==1:
            #     week_reslut[b-1]+=1
            #     week_reslut[a-1]+=1
    #print week_result
    #print sum(week_result)
    for i in range(4):
        week_result[i]=numpy.array(week_result[i])
    plt.figure(facecolor='white')
    times=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(4):
        plt.plot( week_result[i],'o--')
    plt.xlim([-0.1, 11.1])
    plt.ylim([-15,40000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],times)
    #plt.xticks([5,17,29,41],['2012','2013','2014','2015'])
    plt.xlabel('month', fontsize=17)
    plt.ylabel('track number', fontsize=17)
    plt.title('2012-2015', fontsize=17)
    plt.legend(('2012','2013','2014','2015'))
    plt.show()
def plot_checkin_num_per_user():
    result={}
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            try:
                result[user]+=1
            except KeyError:
                result[user]=1
    data={}
    for i in result:
        try:
            data[result[i]]+=1
        except KeyError:
            data[result[i]]=1
    for i in data:
        print i,data[i]

def get_date_list(start,end):
    data=[]
    data.append(start)
    date1 = datetime.datetime.strptime(start, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(end, '%Y-%m-%d')
    i = datetime.timedelta(days=1)
    while i <= (date2 - date1):
        #print (date1 + i).strftime('%Y-%m-%d')
        data.append((date1 + i).strftime('%Y-%m-%d'))
        i += datetime.timedelta(days=1)
    return data
def plot_checkin_near_Spring_Festival():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list = get_date_list('2012-01-09', '2012-02-06')  # '2012-01-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list=get_date_list('2013-01-27','2013-02-24') # '2013-02-10'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2014-01-17','2014-02-14')  # new year ,'2014-01-31'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2015-02-05', '2015-03-05')  # new year ,'2015-02-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Spring Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,5000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Spring Festival', fontsize=17)
    plt.plot([14, 14], [0, 5000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_May_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-04-17','2012-05-15')#new year ,'2012-05-01'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-04-17', '2013-05-15')  # new year ,'2013-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-04-17', '2014-05-15')  # new year ,'2014-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-04-17', '2015-05-15')  # new year ,'2012-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'May Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near May Day', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Mid_Autumn_Festival():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-09-16','2012-10-14')#new year ,'2012-09-30'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-09-05', '2013-10-03')  # new year ,'2013-09-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-25', '2014-09-22')  # new year ,'2014-09-08'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-13', '2015-10-11')  # new year ,'2015-09-27'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Mid-Autumn Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,3500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Mid-Autumn Festival', fontsize=17)
    plt.plot([14, 14], [0, 3500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_National_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-09-17','2012-10-15')#new year ,'2012-10-01'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-09-17', '2013-10-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-09-17', '2014-10-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-17', '2015-10-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'National Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,3500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near National Day', fontsize=17)
    plt.plot([14, 14], [0, 3500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_New_Year():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-12-18','2013-01-15')#new year ,'2012-01-01'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-12-18', '2014-01-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-18', '2015-01-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-18', '2016-01-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'New Year',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near New Year', fontsize=17)
    plt.plot([14, 14], [0, 4500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Valentine_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-01-31','2012-02-28')#new year ,'2012-02-14'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-01-31', '2013-02-28')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-01-31', '2015-02-28')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Valentine\'s Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Valentine\'s Day', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Qingming():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-03-21','2012-04-18')#new year ,'2012-04-04'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-03-21', '2013-04-18')  # new year ,'2013-04-04'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-03-22', '2014-02-19')  # new year ,'2014-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-03-22', '2015-02-19')  # new year ,'2015-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Qingming',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,3500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Qingming', fontsize=17)
    plt.plot([14, 14], [0, 3500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Children_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-05-18','2012-06-15')#new year ,'2012-06-01'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-05-18', '2013-06-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-05-18', '2014-06-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-05-18', '2015-06-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Children\'s Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Children\'s Day', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Teachers_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-08-27','2012-09-24')#new year ,'2012-09-10'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-08-27', '2013-09-24')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-27', '2014-09-24')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-27', '2015-09-24')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Teachers\' Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Teachers\' Day', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Christmas():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-12-11','2013-01-08')#new year ,'2012-12-25'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-12-11', '2014-01-08')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-11', '2015-01-08')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-11', '2016-01-08')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Christmas',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Christmas', fontsize=17)
    plt.plot([14, 14], [0, 4500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Double_Seventh():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-08-09','2012-09-06')#new year ,'2012-08-23'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-07-30', '2013-08-27')  # new year ,'2013-08-13'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-07-19', '2014-08-16')  # new year ,'2014-08-02'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-06', '2015-09-03')  # new year ,'2015-08-20'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Double Seventh',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Double Seventh', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Lantern_Festival():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-01-23','2012-02-20')#new year ,'2012-02-06'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-02-10', '2013-03-10')  # new year ,'2013-02-24'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-19', '2015-03-19')  # new year ,'2015-03-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Lantern Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,4000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Lantern Festival', fontsize=17)
    plt.plot([14, 14], [0, 4000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_checkin_near_Tree_planting_Day():
    data=[]
    for i in range(29):
        data.append(0)
    timestamp={}
    date_list=get_date_list('2012-02-27','2012-03-26')#new year ,'2012-03-12'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2013-02-26', '2013-03-26')  # new year ,'2013-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-02-26', '2014-03-26')  # new year ,'2014-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-26', '2015-03-26')  # new year ,'2015-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt','r') as f:
        #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
        for line in f:
            part=line.strip().split(';;')
            user=part[0]
            tt=part[1][0:10]
            try:
                data[timestamp[tt]]+=1
            except KeyError:
                continue
    for i in data:
        print i
    errors = numpy.array(data)
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Tree planting Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    plt.plot( errors)
    plt.xlim([0, 28])
    plt.ylim([0,3500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.title('how many tracks happened near Tree planting Day', fontsize=17)
    plt.plot([14, 14], [0, 3500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()

def plot_track_pattern_near_Spring_Festival():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-09', '2012-02-06')  # '2012-01-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list=get_date_list('2013-01-27','2013-02-24') # '2013-02-10'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2014-01-17','2014-02-14')  # new year ,'2014-01-31'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2015-02-05', '2015-03-05')  # new year ,'2015-02-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Spring Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Spring Festival', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_May_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-04-17', '2012-05-15')  # new year ,'2012-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-04-17', '2013-05-15')  # new year ,'2013-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-04-17', '2014-05-15')  # new year ,'2014-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-04-17', '2015-05-15')  # new year ,'2012-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'May Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near May Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Mid_Autumn_Festival():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-09-16', '2012-10-14')  # new year ,'2012-09-30'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-09-05', '2013-10-03')  # new year ,'2013-09-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-25', '2014-09-22')  # new year ,'2014-09-08'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-13', '2015-10-11')  # new year ,'2015-09-27'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Mid-Autumn Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Mid-Autumn Festival', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_National_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-09-17', '2012-10-15')  # new year ,'2012-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-09-17', '2013-10-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-09-17', '2014-10-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-17', '2015-10-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'National Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near National Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_New_Year():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-18', '2013-01-15')  # new year ,'2012-01-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-18', '2014-01-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-18', '2015-01-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-18', '2016-01-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'New Year',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near New Year', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Valentine_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-31', '2012-02-28')  # new year ,'2012-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-01-31', '2013-02-28')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-01-31', '2015-02-28')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Valentine\' Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Valentine\' Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Qingming():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-03-21', '2012-04-18')  # new year ,'2012-04-04'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-03-21', '2013-04-18')  # new year ,'2013-04-04'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-03-22', '2014-02-19')  # new year ,'2014-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-03-22', '2015-02-19')  # new year ,'2015-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Qingming',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Qingming', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Children_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-05-18', '2012-06-15')  # new year ,'2012-06-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-05-18', '2013-06-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-05-18', '2014-06-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-05-18', '2015-06-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Children Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Children Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Teachers_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-08-27', '2012-09-24')  # new year ,'2012-09-10'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-08-27', '2013-09-24')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-27', '2014-09-24')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-27', '2015-09-24')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Teachers Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Teachers Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Christmas():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-11', '2013-01-08')  # new year ,'2012-12-25'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-11', '2014-01-08')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-11', '2015-01-08')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-11', '2016-01-08')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Christmas',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Christmas', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Double_Seventh():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-08-09', '2012-09-06')  # new year ,'2012-08-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-07-30', '2013-08-27')  # new year ,'2013-08-13'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-07-19', '2014-08-16')  # new year ,'2014-08-02'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-06', '2015-09-03')  # new year ,'2015-08-20'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Double Seventh',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Double Seventh', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Lantern_Festival():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-23', '2012-02-20')  # new year ,'2012-02-06'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-02-10', '2013-03-10')  # new year ,'2013-02-24'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-19', '2015-03-19')  # new year ,'2015-03-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Lantern Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Lantern Festival', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Tree_planting_Day():
    result=[]
    for j in range(6):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-02-27', '2012-03-26')  # new year ,'2012-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-02-26', '2013-03-26')  # new year ,'2013-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-02-26', '2014-03-26')  # new year ,'2014-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-26', '2015-03-26')  # new year ,'2015-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(6):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Tree-planting Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(6):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Tree-planting Day', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()

def compute_track_num_for_8_pattern():
    result = [0,0,0,0,0,0,0,0]#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[0]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[1]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区'):
                    result[2]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area !=u'区' and b_area==u'区'):
                    result[3] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[4]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[5]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') :
                    result[6]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area !=u'区' and b_area==u'区'):
                    result[7] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    total=sum(result)
    # 相同城区内，相同县区内，相同城区与县区，相同县区到城区，不同城区与城区，不同县区与县区，不同城区与县区，不同县区与城区
    title=['相同城市：辖区间：','相同城市：辖县间：','相同城市：辖区与辖县间：','相同城市：辖县与辖区间：',
           '不同城市：辖区间：','不同城市：辖县间：','不同城市：辖区与辖县间：','不同城市：辖县与辖区间：']
    for a in range(0,len(result)):
        print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def compute_user_num_for_8_pattern():
    result = [{},{},{},{},{},{},{},{}]#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[0][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[1][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') :
                    result[2][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area !=u'区' and b_area==u'区'):
                    result[3][a_user] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[4][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[5][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区') :
                    result[6][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area !=u'区' and b_area==u'区'):
                    result[7][a_user]=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    total={}
    for i in result:
        for j in i:
            total[j]=1
    total=len(total)
    for i in range(len(result)):
        result[i]=len(result[i])
    #total=sum(result)
    # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    title = ['相同城市：辖区间：', '相同城市：辖县间：', '相同城市：辖区与辖县间：', '相同城市：辖县与辖区间：',
             '不同城市：辖区间：', '不同城市：辖县间：', '不同城市：辖区与辖县间：', '不同城市：辖县与辖区间：']
    for a in range(0,len(result)):
        print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def get_user_for_8_pattern():
    result = {}#城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line=f.readline()
        part = line.strip().split(';;')
        a_location=part[2]
        a_user=part[0]
        p_part=part[4].split(',')
        a_city=p_part[0].decode('utf-8')
        a_area=p_part[1].decode('utf-8')[-1]
        try:
            uu=len(result[a_user])
        except KeyError:
            result[a_user]=[0,0,0,0,0,0,0,0]
        ii=0
        for line in f:
            ii+=1
            if ii%100==0:
                print ii
            #print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                uu = len(result[b_user])
            except KeyError:
                result[b_user] = [0, 0, 0, 0, 0, 0,0,0]
            try:
                b_area=b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            #print b_area
            if a_user != b_user:
                a_user=b_user
                a_location=b_location
                a_city=b_city
                a_area=b_area
                continue
            if a_city == b_city:

                if a_area ==u'区' and b_area==u'区':
                    result[a_user][0]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[a_user][1]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区'):
                    result[a_user][2]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area !=u'区' and b_area==u'区'):
                    result[a_user][3]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area ==u'区' and b_area==u'区':
                    result[a_user][4]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area !=u'区' and b_area!=u'区':
                    result[a_user][5]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area ==u'区' and b_area!=u'区'):
                    result[a_user][6]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area !=u'区' and b_area==u'区'):
                    result[a_user][7]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    part_result={}
    for each in result:
        total=sum(result[each])
        if total ==0:
            #result.pop(each)
            continue
        for a in range(len(result[each])):
            result[each][a]=(result[each][a]*1.0/total)
        part_result[each]=result[each]
    result=part_result
    with open('../data/ID_8_pattern_ration.txt','w') as ff :
        for a in result:
            ff.write(str(a)+':'+str(result[a])+'\r\n')
    with open('../data/ID_8_pattern_ration_for_weka.arff', 'w') as fw:
        fw.write('@relation pattern\r\n')
        fw.write('@attribute pattern0 real\r\n')
        fw.write('@attribute pattern1 real\r\n')
        fw.write('@attribute pattern2 real\r\n')
        fw.write('@attribute pattern3 real\r\n')
        fw.write('@attribute pattern4 real\r\n')
        fw.write('@attribute pattern5 real\r\n')
        fw.write('@attribute pattern6 real\r\n')
        fw.write('@attribute pattern7 real\r\n')
        fw.write('@data\r\n')
        for a in result:
            fw.write(str(result[a][0])+',' +str(result[a][1])+',' +str(result[a][2])+',' +str(result[a][3])+',' +str(result[a][4])+
                     ',' +str(result[a][5])+',' +str(result[a][6])+',' +str(result[a][7])  + '\r\n')
    #total=sum(result)
    # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # title=['相同城市：辖区间：','相同城市：辖县间：','相同城市：辖区与辖县间：','不同城市：辖区间：','不同城市：辖县间：','不同城市：辖区与辖县间：']
    # for a in range(0,len(result)):
    #     print title[a], result[a],'占比: ',(result[a]*1.0/total)*100,'%'
def plot_cluster_select_and_squared_error_8_pattern():
    times=[]
    errors=[]
    with open('../data/cluster_select_and_squared_error_8_pattern.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            times.append(int(part[0]))
            errors.append(float(part[1]))
    errors=numpy.array(errors)
    plt.figure(facecolor='white')
    plt.plot(times,errors)
    plt.xlim([1,20])
    plt.ylim([0,30000])
    plt.xticks(times,fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Cluster',fontsize=17)
    plt.ylabel('Squared Error',fontsize=17)
    plt.title('how many clusters do fit ?',fontsize=17)
    plt.plot([4,4], [0, 9390.360745822429], color='red', linewidth=2.5, linestyle="--")
    plt.plot([0, 4], [9390.360745822429, 9390.360745822429], color='red', linewidth=2.5, linestyle="--")
    #plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def get_ID_cluster_for_8_pattern():
    user=[]
    cluster=[]
    with open('../data/ID_8_pattern_ration.txt','r') as f:
        for line in f:
            user.append(line.split(':')[0])
    with open('../data/cluster_result_8_pattern.txt','r') as f:
        for line in f:
            #print '11111',line
            cluster.append(line.strip().split('cluster')[1])
    result=[0,0,0,0]
    with open('../data/ID_cluster_8_pattern.txt','w') as f:
        for i in range(len(user)):
            f.write(user[i]+','+cluster[i]+'\r\n')
            result[int(cluster[i])]+=1
    total=sum(result)
    for a in result:
        print a, a*1.0/total*100
def plot_median_for_4_cluster_in_8_pattern():
    result=[]
    for i in range(4):
        result.append([])
        for j in range(8):
            result[-1].append([])
    user_cluster={}
    with open('../data/ID_cluster_8_pattern.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            user_cluster[part[0]]=part[1]
    with open('../data/ID_8_pattern_ration.txt','r') as f:
        for line in f:
            part=line.strip().split(':')
            user=part[0]
            data=eval(part[1])
            for a in range(len(data)):
                result[int(user_cluster[user])][a].append(data[a])
    for i in range(4):
        for j in range(8):
            try:
                result[i][j]=(sum(result[i][j])*1.0/len(result[i][j]))
            except ZeroDivisionError:
                result[i][j]=0
    for i in range(4):
        result[i]=numpy.array(result[i])
        print result[i]
    N = 8
    plt.figure(facecolor='white')
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    color=['r','g','b','gray']
    pp=[0,0,0,0]
    for i in range(4):
        pp[i]=plt.bar(ind+width*i, result[i], width, color=color[i])

    # add some text for labels, title and axes ticks
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')
    plt.xlim([-0.4,8])
    plt.yticks(fontsize=13)
    plt.xticks(ind + width*1.5,(r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
                                r'$A_d<->B_d$', r'$A_c<->B_c$',r'$A_d<->B_c$',r'$A_c<->B_d$'),fontsize=14)
    #plt.xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.xlabel('pattern',fontsize=16)
    plt.ylabel('average ratio',fontsize=16)
    plt.title('cluster distribution in different patterns',fontsize=18)
    plt.legend(pp, ('Cluster-0', 'Cluster-1','Cluster-2','Cluster-3'),fontsize=17)
    plt.show()

def plot_track_pattern_near_Spring_Festival_8_pattern():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-09', '2012-02-06')  # '2012-01-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list=get_date_list('2013-01-27','2013-02-24') # '2013-02-10'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2014-01-17','2014-02-14')  # new year ,'2014-01-31'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2015-02-05', '2015-03-05')  # new year ,'2015-02-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Spring Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(8):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$',r'$A_c<->A_d$',
                                   r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Spring Festival', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Christmas_8_pattern():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-11', '2013-01-08')  # new year ,'2012-12-25'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-11', '2014-01-08')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-11', '2015-01-08')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-11', '2016-01-08')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Christmas',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(8):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Christmas', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_New_Year_8_pattern():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-18', '2013-01-15')  # new year ,'2012-01-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-18', '2014-01-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-18', '2015-01-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-18', '2016-01-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    if a_location == b_location:
                        a_user = b_user
                        a_city = b_city
                        a_area = b_area
                        a_location = b_location
                        continue
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') or (a_area != u'区' and b_area == u'区'):
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'New Year',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(8):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near New Year', fontsize=17)
    plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_National_Day_8_pattern():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-09-17', '2012-10-15')  # new year ,'2012-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-09-17', '2013-10-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-09-17', '2014-10-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-17', '2015-10-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'National Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(8):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,2000])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near National Day', fontsize=17)
    plt.plot([14, 14], [0, 2000], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()
def plot_track_pattern_near_Lantern_Festival_8_pattern():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-23', '2012-02-20')  # new year ,'2012-02-06'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-02-10', '2013-03-10')  # new year ,'2013-02-24'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-19', '2015-03-19')  # new year ,'2015-03-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        result[i] = numpy.array(result[i])
    plt.figure(facecolor='white')
    times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
           'Lantern Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    gg=[]
    for i in range(8):
        gg.append(plt.plot(result[i]))
    plt.xlim([0, 28])
    plt.ylim([0,1500])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    plt.yticks(fontsize=13)
    plt.xlabel('Day', fontsize=17)
    plt.ylabel('Number', fontsize=17)
    plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    plt.title('how many tracks happened near Lantern Festival', fontsize=17)
    plt.plot([14, 14], [0, 1500], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    plt.show()

def plot_track_pattern_near_National_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-09-17', '2012-10-15')  # new year ,'2012-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-09-17', '2013-10-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-09-17', '2014-10-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-17', '2015-10-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total=sum(result[i])
        for j in range(29):
            result[i][j]=(result[i][j]*1.0/total)
    for i in range(8):
        result[i] = numpy.array(result[i])
    #plt.figure(facecolor='white')

    a = numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
    b = numpy.array([1,2,3,4,5,6,7,8,9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label=['14',' ',' ',' ',' ',' ',' ','7',' ',' ',' ',' ',' ',' ',
            'National Day',' ',' ',' ',' ',' ',' ','7',' ',' ',' ',' ',' ',' ','14']
    plt.xticks([0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,
                15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,23.5,24.5,25.5,26.5,27.5,28.5],x_label,fontsize=13)
    y_label=[r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
                 r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5],y_label,fontsize=13)
    plt.title('how many tracks happened near National Day', fontsize=17)
    plt.show()


    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'National Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,0.1])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
    #             r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near National Day', fontsize=17)
    # plt.plot([14, 14], [0, 0.1], color='red', linewidth=1.5, linestyle="--")
    #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    #plt.show()
def plot_track_pattern_near_Lantern_Festival_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-23', '2012-02-20')  # new year ,'2012-02-06'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-02-10', '2013-03-10')  # new year ,'2013-02-24'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-19', '2015-03-19')  # new year ,'2015-03-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            result[i][j] = (result[i][j] * 1.0 / total)
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Lantern Festival', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ', '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Lantern Festival', fontsize=17)
    plt.show()
    # for i in range(8):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Lantern Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1500])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
    #             r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Lantern Festival', fontsize=17)
    # plt.plot([14, 14], [0, 1500], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_New_Year_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-18', '2013-01-15')  # new year ,'2012-01-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-18', '2014-01-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-18', '2015-01-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-18', '2016-01-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            result[i][j] = (result[i][j] * 1.0 / total)
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'New Year', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near New Year', fontsize=17)
    plt.show()
    # for i in range(8):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'New Year',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
    #             r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near New Year', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Spring_Festival_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-09', '2012-02-06')  # '2012-01-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list=get_date_list('2013-01-27','2013-02-24') # '2013-02-10'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2014-01-17','2014-02-14')  # new year ,'2014-01-31'
    for i in date_list:
        timestamp[i]=date_list.index(i)
    date_list = get_date_list('2015-02-05', '2015-03-05')  # new year ,'2015-02-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区'):
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area != u'区' and b_area == u'区') :
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j]=0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Spring Festival', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Spring Festival', fontsize=17)
    plt.show()
    # for i in range(8):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Spring Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$',r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Spring Festival', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Christmas_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-12-11', '2013-01-08')  # new year ,'2012-12-25'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-12-11', '2014-01-08')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-12-11', '2015-01-08')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-12-11', '2016-01-08')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Christmas', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Christmas', fontsize=17)
    plt.show()
    # for i in range(8):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Christmas',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend((r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d<->A_c$', r'$A_c<->A_d$',
    #             r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Christmas', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_May_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-04-17', '2012-05-15')  # new year ,'2012-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-04-17', '2013-05-15')  # new year ,'2013-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-04-17', '2014-05-15')  # new year ,'2014-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-04-17', '2015-05-15')  # new year ,'2012-05-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'May Day', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near May Day', fontsize=17)
    plt.show()
    # for i in range(8):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'May Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(8):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near May Day', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Mid_Autumn_Festival_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-09-16', '2012-10-14')  # new year ,'2012-09-30'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-09-05', '2013-10-03')  # new year ,'2013-09-19'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-25', '2014-09-22')  # new year ,'2014-09-08'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-09-13', '2015-10-11')  # new year ,'2015-09-27'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Mid Autumn Festival', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Mid Autumn Festival', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Mid-Autumn Festival',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Mid-Autumn Festival', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Valentine_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-01-31', '2012-02-28')  # new year ,'2012-02-14'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-01-31', '2013-02-28')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-01-31', '2014-02-28')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-01-31', '2015-02-28')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Valentine Day', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Valentine Day', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Valentine\' Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Valentine\' Day', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Qingming_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-03-21', '2012-04-18')  # new year ,'2012-04-04'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-03-21', '2013-04-18')  # new year ,'2013-04-04'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-03-22', '2014-02-19')  # new year ,'2014-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-03-22', '2015-02-19')  # new year ,'2015-04-05'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Qingming', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Qingming', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Qingming',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Qingming', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Children_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-05-18', '2012-06-15')  # new year ,'2012-06-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-05-18', '2013-06-15')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-05-18', '2014-06-15')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-05-18', '2015-06-15')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':

                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Children\'s Day', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Children\'s Day', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Children Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Children Day', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Teachers_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-08-27', '2012-09-24')  # new year ,'2012-09-10'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-08-27', '2013-09-24')  # new year ,'2013-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-08-27', '2014-09-24')  # new year ,'2014-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-27', '2015-09-24')  # new year ,'2015-10-01'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Teachers\' Day', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Teachers\' Day', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Teachers Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Teachers Day', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Double_Seventh_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-08-09', '2012-09-06')  # new year ,'2012-08-23'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-07-30', '2013-08-27')  # new year ,'2013-08-13'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-07-19', '2014-08-16')  # new year ,'2014-08-02'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-08-06', '2015-09-03')  # new year ,'2015-08-20'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Double Seventh', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Double Seventh', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Double Seventh',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Double Seventh', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()
def plot_track_pattern_near_Tree_planting_Day_8_pattern_ratio_heatmap():
    result=[]
    for j in range(8):
        result.append([])
        for k in range(29):
            result[-1].append(0)
    timestamp={}
    date_list = get_date_list('2012-02-27', '2012-03-26')  # new year ,'2012-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2013-02-26', '2013-03-26')  # new year ,'2013-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2014-02-26', '2014-03-26')  # new year ,'2014-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    date_list = get_date_list('2015-02-26', '2015-03-26')  # new year ,'2015-03-12'
    for i in date_list:
        timestamp[i] = date_list.index(i)
    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][timestamp[b_time]] += 1
                    except KeyError:
                        pass
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        total = sum(result[i])
        for j in range(29):
            try:
                result[i][j] = (result[i][j] * 1.0 / total)
            except ZeroDivisionError:
                result[i][j] = 0
    for i in range(8):
        result[i] = numpy.array(result[i])
    a = numpy.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29])
    b = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    a, b = numpy.meshgrid(a, b)
    fig, ax = plt.subplots()
    im = ax.pcolormesh(a, b, result)
    fig.colorbar(im)
    plt.plot([14.5, 14.5], [1, 9], color='red', linewidth=2.5, linestyle="--")
    ax.axis('tight')
    x_label = ['14', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               'Tree planting Day', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' ', ' ', ' ', ' ', ' ', ' ',
               '14']
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5,
                15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5],
               x_label, fontsize=13)
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.yticks([1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5], y_label, fontsize=13)
    plt.title('how many tracks happened near Tree planting Day', fontsize=17)
    plt.show()
    # for i in range(6):
    #     result[i] = numpy.array(result[i])
    # plt.figure(facecolor='white')
    # times=['14',' ','12',' ','10',' ','8',' ','6',' ','4',' ','2',' ',
    #        'Tree-planting Day',' ','2',' ','4',' ','6',' ','8',' ','10',' ','12',' ','14']
    # gg=[]
    # for i in range(6):
    #     gg.append(plt.plot(result[i]))
    # plt.xlim([0, 28])
    # plt.ylim([0,1000])
    # plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],times,fontsize=13)
    # plt.yticks(fontsize=13)
    # plt.xlabel('Day', fontsize=17)
    # plt.ylabel('Number', fontsize=17)
    # plt.legend( (r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_c<->A_d$',
    #                                r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_c<->B_d$'), fontsize=13)
    # plt.title('how many tracks happened near Tree-planting Day', fontsize=17)
    # plt.plot([14, 14], [0, 1000], color='red', linewidth=1.5, linestyle="--")
    # #plt.plot([4, 4], [0, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # #plt.plot([0, 4], [9240.367340507137, 9240.367340507137], color='red', linewidth=2.5, linestyle="--")
    # # plt.axis([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # plt.show()

def plot_gender_distribution_for_4_cluster_8_pattern():
    result={'男':[0,0,0,0],'女':[0,0,0,0]}
    user_cluster={}
    with open('../data/ID_cluster_8_pattern.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            user_cluster[part[0]]=int(part[1])
    with open('../data/query_result.txt','r') as f:
        #"ID","注册时间","性别","所在地","粉丝","关注","微博","标签","性取向","感情状况",
        # "生日","血型","大学","高中","初中","小学","中专技校","公司","邮箱"
        f.readline()
        for line in f:
            part=line.strip().split(',')
            sex=part[2]
            user=part[0]
            #print sex
            try:
                result[sex][user_cluster[user]]+=1
            except KeyError:
                continue
    for a in range(4):
        total=result['男'][a]+result['女'][a]
        result['男'][a]=(result['男'][a]*1.0/total)
        result['女'][a]=(result['女'][a]*1.0/total)
    for a in result:
        print a,result[a]
    data=[result['男'],result['女']]
    N = 4
    plt.figure(facecolor='white')
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    color = ['b', 'r']
    pp = [0, 0]
    for i in range(2):
        pp[i] = plt.bar(ind + width * i, data[i], width, color=color[i])

    # add some text for labels, title and axes ticks
    # ax.set_ylabel('Scores')
    # ax.set_title('Scores by group and gender')
    plt.xlim([-0.4, 3.6])
    plt.yticks(fontsize=13)
    plt.xticks(ind + width * 0.5, (r'cluster 0', r'cluster 1', r'cluster 2', r'cluster 3'), fontsize=14)
    # plt.xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.xlabel('Cluster', fontsize=16)
    plt.ylabel('ratio', fontsize=16)
    plt.title('gender distribution for different clusters', fontsize=18)
    plt.legend(pp, ('Male', 'Female',), fontsize=17)
    plt.show()
def plot_age_distribution_for_4_cluster_8_pattern():
    result={6:[0,0,0,0],7:[0,0,0,0],8:[0,0,0,0],9:[0,0,0,0],0:[0,0,0,0]}
    user_cluster={}
    with open('../data/ID_cluster_8_pattern.txt','r') as f:
        for line in f:
            part=line.strip().split(',')
            user_cluster[part[0]]=int(part[1])
    with open('../data/query_result.txt','r') as f:
        #"ID","注册时间","性别","所在地","粉丝","关注","微博","标签","性取向","感情状况",
        # "生日","血型","大学","高中","初中","小学","中专技校","公司","邮箱"
        f.readline()
        for line in f:
            part=line.strip().split(',')
            try:
                age=int(part[10][2])
            except IndexError:
                #print part[10]
                continue
            except ValueError:
                #print part[10]
                continue
            user=part[0]
            #print sex
            try:
                result[age][user_cluster[user]]+=1
            except KeyError:
                continue
    for i in result:
        print i,result[i]
    data=[result[6],result[7],result[8],result[9],result[0]]
    data=numpy.array(data)
    N = 4
    plt.figure(facecolor='white')
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.15  # the width of the bars
    color = ['r', 'g','b','y','grey']
    pp = [0, 0,0,0,0]
    for i in range(5):
        pp[i] = plt.bar(ind + width * i, data[i], width, color=color[i])
    plt.xlim([-0.3, 4])
    plt.yticks(fontsize=13)
    plt.xticks(ind + width * 2, (r'cluster 0', r'cluster 1', r'cluster 2', r'cluster 3'), fontsize=14)
    # plt.xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.xlabel('Cluster', fontsize=16)
    plt.ylabel('Number', fontsize=16)
    plt.title('Age distribution for different clusters', fontsize=18)
    plt.legend(pp, ('1960s','1970s','1980s','1990s','2000s',), fontsize=17)
    plt.show()
def plot_top_10_track_for_8_pattern_city_level():
    result=[]
    for j in range(8):
        result.append({})

    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[0][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[1][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[2][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[3][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[4][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[5][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[6][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][a_city+'->'+b_city] += 1
                    except KeyError:
                        result[7][a_city + '->' + b_city] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue

    for i in range(8):
        result[i]=sorted(result[i].iteritems(),key=lambda d:d[1],reverse=True)
    y_label = [r'A_d<->A_d', r'A_c<->A_c', r'A_d ->A_c', r'A_c ->A_d',
               r'A_d<->B_d', r'A_c<->B_c', r'A_d ->B_c', r'A_c ->B_d']
    for i in range(8):
        for j in range(3):
            print y_label[i],j,result[i][j][0],result[i][j][1]
        print
def plot_top_10_track_for_8_pattern_area_level():
    result=[]
    for j in range(8):
        result.append({})

    #result = [0, 0, 0, 0, 0, 0]  # 城区内，县区内，相同城区与县区，城区与城区，县区与县区，不同城区与县区
    # 1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        a_a=p_part[1].decode('utf-8')
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
                b_a=b_p_part[1].decode('utf-8')
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                a_a=b_a
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[0][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[0][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[1][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[1][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[2][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[2][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[3][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[3][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    try:
                        result[4][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[4][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    try:
                        result[5][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[5][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    try:
                        result[6][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[6][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    try:
                        result[7][a_city+'.'+a_a+'->'+b_city+'.'+b_a] += 1
                    except KeyError:
                        result[7][a_city+'.'+a_a+'->'+b_city+'.'+b_a] = 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_a=b_a
                    a_location = b_location
                    continue

    for i in range(8):
        result[i]=sorted(result[i].iteritems(),key=lambda d:d[1],reverse=True)
    y_label = [r'A_d<->A_d', r'A_c<->A_c', r'A_d ->A_c', r'A_c ->A_d',
               r'A_d<->B_d', r'A_c<->B_c', r'A_d ->B_c', r'A_c ->B_d']
    for i in range(8):
        for j in range(5):
            print y_label[i],j,result[i][j][0],result[i][j][1]
        print
def get_checkin_area_per_user():
    result={}
    ii = 0
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        for line in f:
            if ii%1000==0:
                print ii
            ii+=1
            part = line.strip().split(';;')
            a_location = part[2]
            a_user = part[0]
            a_time=part[1][0:10]
            p_part = part[4].split(',')
            a_city = p_part[0].decode('utf-8')
            try:
                a_area = p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            a_a=p_part[1].decode('utf-8')
            try:
                result[a_user][a_city]+=1
            except KeyError:
                try:
                    result[a_user][a_city]=1
                except KeyError:
                    result[a_user]={}
                    result[a_user][a_city]=1
    for a in result:
        for b in result[a]:
            print a,b,result[a][b]
def plot_per_track_in_7_day_8_pattern():
    pattern_day=[]
    for i in range(8):
        pattern_day.append([])
        for j in range(7):
            pattern_day[-1].append(0)
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=part[1][0:10]
        a_time=datetime.datetime.strptime(a_time,'%Y-%m-%d').weekday()
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=part[1][0:10]
            b_time = datetime.datetime.strptime(b_time, '%Y-%m-%d').weekday()
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    pattern_day[0][b_time]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    pattern_day[1][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    pattern_day[2][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    pattern_day[3][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    pattern_day[4][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    pattern_day[5][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    pattern_day[6][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    pattern_day[7][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        print i, pattern_day[i]
        pattern_day[i]=numpy.array(pattern_day[i])
    plt.figure(facecolor='white')
    for i in range(8):
        plt.plot(pattern_day[i])
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.legend(y_label)
    plt.show()
def plot_per_track_in_24_hour_8_pattern():
    pattern_day=[]
    for i in range(8):
        pattern_day.append([])
        for j in range(24):
            pattern_day[-1].append(0)
    #1000900020;;2014-09-29 13:18;;[120.58529,31.298979];;['China', 'Jiangsu', 'Suzhou'];;苏州市,姑苏区,320502
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        line = f.readline()
        part = line.strip().split(';;')
        a_location = part[2]
        a_user = part[0]
        a_time=int(part[1][11:13])
        #a_time=datetime.datetime.strptime(a_time,'%Y-%m-%d').weekday()
        p_part = part[4].split(',')
        a_city = p_part[0].decode('utf-8')
        a_area = p_part[1].decode('utf-8')[-1]
        ii = 0
        for line in f:
            ii += 1
            if ii % 100 == 0:
                print ii
            # print line
            part = line.strip().split(';;')
            b_location = part[2]
            b_user = part[0]
            b_time=int(part[1][11:13])
            #b_time = datetime.datetime.strptime(b_time, '%Y-%m-%d').weekday()
            b_p_part = part[4].split(',')
            b_city = b_p_part[0].decode('utf-8')
            try:
                b_area = b_p_part[1].decode('utf-8')[-1]
            except IndexError:
                continue
            # print b_area
            if a_user != b_user:
                a_user = b_user
                a_location = b_location
                a_city = b_city
                a_area = b_area
                a_time=b_time
                continue
            if a_city == b_city:
                if a_area == u'区' and b_area == u'区':
                    pattern_day[0][b_time]+=1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    a_time=b_time
                    continue
                if a_area != u'区' and b_area != u'区':
                    pattern_day[1][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    pattern_day[2][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    pattern_day[3][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
            if a_city != b_city:
                if a_area == u'区' and b_area == u'区':
                    pattern_day[4][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if a_area != u'区' and b_area != u'区':
                    pattern_day[5][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if (a_area == u'区' and b_area != u'区') :
                    pattern_day[6][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
                if  (a_area != u'区' and b_area == u'区'):
                    pattern_day[7][b_time] += 1
                    a_user = b_user
                    a_city = b_city
                    a_area = b_area
                    a_location = b_location
                    continue
    for i in range(8):
        print i, pattern_day[i]
        pattern_day[i]=numpy.array(pattern_day[i])
    plt.figure(facecolor='white')
    for i in range(8):
        plt.plot(pattern_day[i])
    y_label = [r'$A_d<->A_d$', r'$A_c<->A_c$', r'$A_d ->A_c$', r'$A_c ->A_d$',
               r'$A_d<->B_d$', r'$A_c<->B_c$', r'$A_d ->B_c$', r'$A_c ->B_d$']
    plt.legend(y_label)
    plt.show()
def Permanent_residence_reasoning():
    result = {}
    user_num={}
    ii = 0
    with open('../data/valid_id_timestamp_jingweidu_country_province_city_zipcode.txt', 'r') as f:
        for line in f:
            if ii % 10000 == 0:
                print ii
            ii += 1
            part = line.strip().split(';;')
            a_location = part[2]
            a_user = part[0]
            a_time = part[1][0:10]
            p_part = part[4].split(',')
            a_city = p_part[0].decode('utf-8')
            a_area = p_part[1].decode('utf-8')
            try:
                user_num[a_user]+=1
            except KeyError:
                user_num[a_user]=1
            try:
                result[a_user][a_city][a_area] += 1
            except KeyError:
                try:
                    result[a_user][a_city][a_area] = 1
                except KeyError:
                    try:
                        result[a_user][a_city] = {}
                        result[a_user][a_city][a_area]=1
                    except KeyError:
                        result[a_user]={}
                        result[a_user][a_city] = {}
                        result[a_user][a_city][a_area] = 1
    num_more_than_10=0
    for i in user_num:
        if user_num[i]>=5:
            num_more_than_10+=1
            for j in result[i]:
                city_num=0
                for k in result[i][j]:
                    city_num+=result[i][j][k]
                
    print num_more_than_10,len(user_num),num_more_than_10*100.0/len(user_num)
if __name__=='__main__':
    data=[
        [0.1,0.1],
        [0.1, 0.1,0.8],
        [0.2,0.2],
        [0.3, 0.3],
        [0.4, 0.4],
        [0.5,0.5],
        [0.6,0.6],
        [0.6,0.6,0.6],
        [1,1,1,1],
        [1],
        [2]


    ]
    for i in data:
        print entropy(i)

    #Permanent_residence_reasoning()
    #plot_per_track_in_24_hour_8_pattern()
    #get_checkin_area_per_user()
    #plot_top_10_track_for_8_pattern_area_level()
    #plot_track_pattern_near_Tree_planting_Day_8_pattern_ratio_heatmap()
    #plot_track_pattern_near_Spring_Festival_8_pattern()
    #plot_gender_distribution_for_4_cluster_8_pattern()
    #plot_median_for_4_cluster_in_8_pattern()
    #get_ID_cluster_for_8_pattern()
    #plot_cluster_select_and_squared_error_8_pattern()
    #get_user_for_8_pattern()
    #compute_user_num_for_8_pattern()
    #compute_track_num_for_8_pattern()
    #plot_track_pattern_near_Tree_planting_Day()
    #plot_track_near_Tree_planting_Day()
    #plot_checkin_num_per_user()
    #plot_gender_distribution_for_4_cluster()
    #plot_per_track_in_per_month_in_12_15()
    #plot_per_track_in_which_month()
    #checkin_of_per_hour_each_city()
    #checkin_of_per_month_each_city()
    #checkin_entropy_of_each_city()
    #a=[0.2,0.2,0.2,0.2,0.2]
    #print entropy(a)
    #get_unique_valid_lat_lng()
    #decode_location()
    #match_city_and_town_and_zip()
    #get_valid_data()
    #crawl_zipcode()
    #compute_num_per_zipcode()
    #compute_checkin_num_in_qu_and_xian_of_per_city()
    #compute_user_num_in_qu_and_xian_of_per_city()
    #compute_different_path()
    #compute_user_num_for_differnt_pattern()
    #get_user_for_per_pattern()
    #plot_cluster_select_and_squared_error()
    #get_ID_cluster()
    #plot_median_for_4_cluster_in_6_pattern()

