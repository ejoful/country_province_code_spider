# -*-coding:utf-8-*-

import scrapy
import os
import csv

url = "https://en.wikipedia.org/wiki/ISO_3166-2:"
country_dic = {}
file_name = ""


class provincecode(scrapy.Spider):
  name = "provincecode"

  # start_urls = [
  #   "https://en.wikipedia.org/wiki/ISO_3166-2"
  # ]

  def start_requests(self):
    urls = [
      "https://en.wikipedia.org/wiki/ISO_3166-2"
    ]
    global file_name
    file_name = os.getcwd() + "/" + getattr(self, 'file_name', None)
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse_country)

  def parse_country(self, response):
    trs = response.css("table.wikitable").css("tbody").css("tr")
    for i in range(len(trs)):
      index = i + 1
      country_code = trs[index].css('td')[0].css("a::text").extract()[0]
      country_name = trs[index].css('td')[1].css("a::text").extract()[0]
      country_dic[country_code] = country_name
      new_url = url + country_code
      yield scrapy.Request(url=new_url, callback=self.parse_province)

  def parse_province(self, response):
    trs = response.css("table.wikitable.sortable").css("tbody").css("tr")

    infos = []
    for i in range(len(trs)):
      index = i + 1
      if index == len(trs):
        break
      print(trs[index])
      province_full_code = trs[index].css("td")[0].css("span::text").extract()[
        0]
      province_name = trs[index].css('td')[1].css("a::text").extract()[0]
      print("province code", province_full_code, province_name, index)
      arr = str.split(province_full_code, "-")
      country_code = arr[0]
      province_code = "-"
      if len(arr) > 1:
        province_code = arr[1]
      country_name = country_dic[country_code]
      info = [country_code, country_name, province_code, province_name,
              province_full_code]
      infos.append(info)

    self.write_file(infos)

  def write_file(self, infos):
    print(file_name)
    with open(file_name, "a") as f:
      writer = csv.writer(f)
      writer.writerows(infos)
