#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# book-master web scraping program

import os
from typing import List
from postgrest import APIError
import requests
from bs4 import BeautifulSoup as bs, Tag
from supabase.client import create_client, Client

rootUrl = "http://books.toscrape.com/"
page = requests.get(rootUrl)

soup = bs(page.content, "html.parser")


supabaseUrl = os.environ.get("SUPABASE_URL")
supabaseServiceKey = os.environ.get("SUPABASE_KEY")

if supabaseUrl and supabaseServiceKey:
    supabase: Client = create_client(supabaseUrl, supabaseServiceKey)
else:
    print("Please set the SUPABASE_URL and SUPABASE_KEY environment variables")
    exit()


def insertBook(book: dict):
    try:
        data = supabase.table("book").select("*").eq("title", book["title"]).execute()
    except APIError as e:
        print(e)
        return
    if len(data.data) > 0:
        print(data, "book(s) found with title", book["title"])
        return
    else:
        try:
            print("Inserting book:", book["title"])
            supabase.table("book").insert(book).execute()
        except APIError as e:
            print(e)
            return


def fetchBookInfo(url: str, category: str):
    book = {
        "title": "",
        "price": 0,
        "rating": 0,
        "category": category,
        "description": "",
        "upc": "",
        "availability": 0,
        "image_link": None,
    }

    page = requests.get(url)
    soup = bs(page.content, "html.parser")

    productMain = soup.find("div", class_="product_main")
    if not isinstance(productMain, Tag):
        return
    titleContainer = productMain.find("h1")
    if isinstance(titleContainer, Tag):
        book["title"] = titleContainer.getText()
    priceContainer = productMain.find("p", class_="price_color")
    if isinstance(priceContainer, Tag):
        book["price"] = float(priceContainer.getText()[1:])
    ratingContainer = productMain.find("p", class_="star-rating")
    if isinstance(ratingContainer, Tag):
        ratingArr = ratingContainer.get("class")
        if isinstance(ratingArr, List):
            if ratingArr[1] == "One":
                book["rating"] = 1
            elif ratingArr[1] == "Two":
                book["rating"] = 2
            elif ratingArr[1] == "Three":
                book["rating"] = 3
            elif ratingArr[1] == "Four":
                book["rating"] = 4
            elif ratingArr[1] == "Five":
                book["rating"] = 5

    productPage = soup.find("article", class_="product_page")
    if not isinstance(productPage, Tag):
        return
    descriptionContainer = productPage.findChild("p", recursive=False)
    if isinstance(descriptionContainer, Tag):
        book["description"] = descriptionContainer.getText()

    infoTable = soup.find("table", class_="table table-striped")
    if not isinstance(infoTable, Tag):
        return
    infoRows = infoTable.find_all("td")
    if isinstance(infoRows[0], Tag):
        book["upc"] = infoRows[0].getText()
    if isinstance(infoRows[5], Tag):
        availabilityStr = infoRows[5].getText()
        book["availability"] = int(
            "".join(list(filter(lambda dig: dig.isdecimal(), availabilityStr)))
        )

    imageContainer = soup.find("img")
    if isinstance(imageContainer, Tag):
        imageSrc = imageContainer.get("src")
        if isinstance(imageSrc, str):
            book["image_link"] = rootUrl + imageSrc[6:]

    insertBook(book)


def fetchByCategories(name: str, position: int):
    url = (
        rootUrl
        + "/catalogue/category/books/"
        + name.lower().replace(" ", "-")
        + "_"
        + str(position + 2)
        + "/index.html"
    )
    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    bookUrls = list(
        map(lambda book: rootUrl + "catalogue/" + book.h3.a.get("href")[9:], books)
    )
    for bookUrl in bookUrls:
        fetchBookInfo(bookUrl, name)


def fetchBooks():
    sideCategories = soup.find_all("div", class_="side_categories")[0]
    categoriesList = sideCategories.findChild().ul.find_all("li")
    categories = list(
        map(
            lambda name: name.replace("\n", "").strip(),
            list(map(lambda tag: tag.a.getText(), categoriesList)),
        ),
    )
    for i in range(len(categories)):
        fetchByCategories(categories[i], i)


fetchBooks()
