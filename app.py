#imports
import streamlit as st
import joblib
import pandas as pd
import random
import re
import datetime
from owlready2 import *
import textwrap


def sayGreeting():
    replies = [
        "Hi! What places can I help you look for? 😄 ",
        "Hello! Where do you want to find places for? 🌴",
        "What's up! Tell me what kind of place you're looking for 😀",
        "Wassup! 😄 ",
        "Sup! What city are you looking to stay in? 😀",
        "Hey hey! 😀 ",
        "Hey! What location can I help you find places to stay? 🏡",
        "Hi, how can I help you? 😀 ",
        "Hello, what can I do for you? 😀 ",
        "Greetings! What kind of place would you like to look for? 🏡 ",
        "Hey! What kind of place are you looking to stay at? 😄 ",
        "'Sup! Where and when are we going? 🏡 "        
    ]
    return random.choice(replies)

def showGratitude():
    replies = [
        "You're welcome! 😊",
        "Glad to be of service! 😃",
        "You are welcome! ☺️",
        "No problem 😀",
        "Of course, you got it! ☺️",
        "Happy to help! 😗",
        "You got it! 😉",
        "You're very welcome! 😁 "       
    ]
    return random.choice(replies)

def sayBye():
    replies = [
        "Bye! ✌️  ",
        "Goobye! 👋 ",
        "See ya! ✌️  ",
        "See you later! 👋 ",
        "Bye bye! 👋 ",
        "Until next time 👋 ",
        "Bye for now! 👋 ",
        "See you next time! ✌️  "
    ]
    return random.choice(replies)

def requestHelp():
    return """
        I'm here to help you find a great place for your next vacation! 😃

        Ask to see places like this:  
        *"I'm looking for places in Osaka for July 1-3"*
        
        If you'd like to check out all our locations, amenities, property types, booking policies, or guest ratings, try this:  
        *"Show me all your ________"*

        Get started, and I'll help match you with the best options!
    """

def getInformation(query):  
    query = query.lower() 
    results = [] 
    info = ""
    if "locations" in query or "cities" in query:
        for location in onto.Location.instances():
            results.append(location.hasCity)
        info = "cities"
    elif "property types" in query:
        for prop in onto.PropertyType.instances():
            results.append(prop.name)
        info = "property types"
    elif "booking policies" in query:
        for policy in onto.BookingPolicy.instances():
            results.append(f"{policy.name}: {policy.hasPolicyDescription}")
        info = "booking policies"
    elif "amenities" in query:
        for amenity in onto.Amenity.instances():
            results.append(amenity.name)
        info = "amenities"
    elif "guest rating" in query or "rating system" in query or "ratings" in query:
        for rating in onto.GuestRating.instances():
            results.append(rating.name)
        info = "guest ratings"
    elif "hosts" in query:
        for host in onto.Host.instances():
            results.append(host.hasHostName)
        info = "hosts"
    else:
        return fallback()         
    return f"""
    📃 Our {info} are:
    {", ".join(x for x in results)}
    """

def searchProperties(query):
    query = query.lower()
    amenities = {
        "wi-fi": "Wi-Fi",
        "wifi": "Wi-Fi",
        "aircon": "AirCon",
        "air conditioning": "AirCon",
        "parking": "Parking",
        "pool": "Pool",
        "pet friendly": "PetFriendly"
    }

    ratings = {
        "great stay": "GreatStay",
        "decent stay": "DecentStay",
        "outstanding": "Outstanding",
        "below average": "BelowAverage",
        "disappointing": "Disappointing"
    }

    booking_policies = {
        "flexible": "Flexible",
        "moderate": "Moderate",
        "strict": "Strict"
    }

    property_types = {
        "villa": "Villa",
        "cabin": "Cabin",
        "house": "House",
        "apartment": "Apartment",
        "flat": "Apartment"
    }

    cities = {
        "ankara": "Ankara",
        "berlin": "Berlin",
        "casablanca": "Casablanca",
        "chicago": "Chicago",
        "cordoba": "Cordoba",
        "dallas": "Dallas",
        "edinburgh": "Edinburgh",
        "granada": "Granada",
        "istanbul": "Istanbul",
        "london": "London",
        "melbourne": "Melbourne",
        "munich": "Munich",
        "new york": "New York",
        "osaka": "Osaka",
        "phoenix": "Phoenix",
        "sydney": "Sydney",
        "tokyo": "Tokyo"
    }
    
    month_to_num = {
        "january": 1,
        "jan": 1,
        "february": 2,
        "feb": 2,
        "march": 3,
        "mar": 3,
        "april": 4,
        "apr": 4,
        "may": 5,
        "june": 6,
        "jun": 6,
        "july": 7,
        "jul": 7,
        "august": 8,
        "aug": 8,
        "september": 9,
        "sep": 9,
        "sept": 9,
        "october": 10,
        "oct": 10,
        "november": 11,
        "nov": 11,
        "december": 12,
        "dec": 12
    }
    
    for amenity in amenities:
        if amenity in query:
            if len(slots["amenities"]) < 4:
                slots["amenities"].append(amenities[amenity])
                user_slots["amenities"] += (f"{amenities[amenity]}")
    for city in cities:
        if city in query:
            slots["city"] = cities[city]
            user_slots["city"] = cities[city]
    for rating in ratings:
        if rating in query:
            slots["guest_rating"] = ratings[rating]
            user_slots["guest_rating"] = ratings[rating]
    for policy in booking_policies:
        if policy in query:
            slots["booking_policy"] = booking_policies[policy]
            user_slots["booking_policy"] = booking_policies[policy]
    for proptype in property_types:
        if proptype in query:
            slots["property_type"] = property_types[proptype]
            user_slots["property_type"] = property_types[proptype]
            
    # Extract date 
    months = r"January|February|March|April|May|June|July|August|September|October|November|December"

    date_pattern = re.compile(
        fr"\b(?:(?P<month>{months})\s(?P<dayfrom>\d{{1,2}})\s?(?:-|and)\s?(?P<dayto>\d{{1,2}})"
        r"|"
        fr"(?P<dayfrom2>\d{{1,2}})\s?(?:-|and)\s?(?P<dayto2>\d{{1,2}})\s(?P<month2>{months})"
        r"|"
        fr"(?P<month3>{months})\s(?P<dayfrom3>\d{{1,2}})\s\w+\s(?P<month4>{months})\s(?P<dayto3>\d{{1,2}}))\b",
        re.IGNORECASE
    )

    date_match = date_pattern.search(query)

    if date_match is not None:
        group_dict = date_match.groupdict()

        if group_dict.get('month3'):
            month = date_match.group('month3')
            month2 = date_match.group('month4')
            day_from = int(date_match.group('dayfrom3'))
            day_to = int(date_match.group('dayto3'))

        elif group_dict.get('month'):
            month = date_match.group('month')
            month2 = date_match.group('month')
            day_from = int(date_match.group('dayfrom'))
            day_to = int(date_match.group('dayto'))

        elif group_dict.get('month2'):
            month = date_match.group('month2')
            month2 = date_match.group('month2')
            day_from = int(date_match.group('dayfrom2'))
            day_to = int(date_match.group('dayto2'))
     
        user_slots["dates"] = f"{month.title()} {day_from} - {month2.title()} {day_to}"
        
        slots["date_from"] = datetime.datetime(2026, month_to_num[month], day_from, 0, 0, 0)
        slots["date_to"] = datetime.datetime(2026, month_to_num[month2], day_to, 23, 59, 59)
    
    # Extract price
    price_pattern = re.compile(        
        r"\b(?:(from|between)\s(?P<min_price>\d{1,4})\s(?:and|to)\s(?P<max_price>\d{1,4})"
        r"|"
        r"(?:under|less than)\s(?P<max_price2>\d{1,4}))\b",
        re.IGNORECASE
    )
    
    price_match = price_pattern.search(query)
    
    if price_match is not None:    
        minimum = price_match.group('min_price')
        maximum = price_match.group('max_price') or price_match.group('max_price2')

        if minimum:
            slots["min_price"] = minimum            
        slots["max_price"] = maximum

        user_slots["price_range"] = f"£{minimum if minimum else 0} - £{maximum}"
    
    # Ontology Access        
    results = []

    for prop in onto.Property.instances():
        match = True
        if any(slots.values()):
            if slots['city']:
                if hasattr(prop, "hasLocation") and prop.hasLocation:
                    location = prop.hasLocation
                    if hasattr(location, "hasCity") and location.hasCity:
                        if location.hasCity != slots["city"]:
                            match = False
            if slots['property_type'] and match:
                if hasattr(prop, "hasPropertyType") and prop.hasPropertyType:
                    if prop.hasPropertyType.name != slots['property_type']:
                        match = False
            if slots['guest_rating'] and match:
                if hasattr(prop, "hasGuestRating") and prop.hasGuestRating:
                    if prop.hasGuestRating.name != slots['guest_rating']:
                        match = False
            if slots['booking_policy']:
                if hasattr(prop, "hasBookingPolicy") and prop.hasBookingPolicy:
                    if prop.hasBookingPolicy.name != slots['booking_policy']:
                        match = False
            if slots['min_price'] and match:
                if hasattr(prop, "hasPrice") and prop.hasPrice:
                    if prop.hasPrice < int(slots['min_price']):
                        match = False
            if slots['max_price'] and match:
                if hasattr(prop, "hasPrice") and prop.hasPrice:
                    if prop.hasPrice > int(slots['max_price']):
                        match = False
            if slots['amenities'] and match:
                if hasattr(prop, "hasAmenity") and prop.hasAmenity:
                    propAmenities = [a.name for a in prop.hasAmenity]
                    if not set(slots['amenities']).issubset(set(propAmenities)):
                        match = False
            if slots['date_from'] and match:
                if hasattr(prop, "isAvailableFrom") and prop.isAvailableFrom:
                    if prop.isAvailableFrom > slots["date_from"]:
                        match = False
            if slots['date_to'] and match:
                if hasattr(prop, "isAvailableTo") and prop.isAvailableTo:
                    if prop.isAvailableTo < slots["date_to"]:
                        match = False
            if match:
                results.append(prop)          

    if not results:
        choices = [
            "Searched everywhere, found nothing 😓\n\nTry tweaking those filters!",
            "Looked high and low, but cound't find anything 😒 \n\n Maybe expand your search?",
            "Your search turned up nothing 🚶 \n\n Try changing your filters!",
            "No properties found 🤖 \n\nTweak those filters!"
        ]
        return random.choice(choices)
    else:
        formatted_results = formatResults(results)
        return formatted_results

def formatResults(results):
    all_results = []
    for result in results:
        prop = (
            f"### {result.hasPropertyName}\n\n"
            f"👥  **{result.hasCapacity} guests**\n\n"
            f"📍 *{result.hasPropertyType.name}* in *{result.hasLocation.hasCity}*\n\n"
            f"💷 **£{result.hasPrice}/night**\n\n"
            f"⭐ {result.hasGuestRating.name} rating from {result.hasNumberOfReviews} reviews\n\n"
            f"❗ **{result.hasBookingPolicy.name} booking policy: {result.hasBookingPolicy.hasPolicyDescription}**"
        )
        all_results.append(prop)
    return " 🔎 **Okay, here's what I found:**\n\n" + "\n\n---\n\n".join(all_results)

def fallback():
    replies = [
        "😒 Sorry, I didn't quite understand that, could you please rephrase?\n\n Type \"help\" if you'd like some guidance!",
        "😣 I'm not sure I understood that, mind saying it in a different way?\n\n Type \"help\" if you're stuck or unsure!",
        "😢 Apologies, I didn't get that. Could you try rephrasing?\n\n Type \"help\" if you need assistance!",
        "😕 Hmm, I don't quite understand that, could you try rephrasing?\n\n Type \"help\" if you want to know your options!",
        "😟 I didn't quite catch that, could you say it a bit differently?\n\n Type \"help\" if you need some tips!"
    ]
    return random.choice(replies)

# chatbot
def getIntent(query):
    vQuery = vectorizer.transform([query])
    probs = model.predict_proba(vQuery)[0]
    predicted_intent = model.classes_[probs.argmax()]
    predicted_confidence = probs.max()

    intent_funcs = {
        "sayGreeting": sayGreeting,
        "showGratitude": showGratitude,
        "sayBye": sayBye,
        "requestHelp": requestHelp,
        "searchProperties": searchProperties,
        "getInformation": getInformation
    }

    if predicted_confidence < 0.85:
        st.session_state.search_intent = False
        return fallback()
    else:
        if predicted_intent == "searchProperties" or predicted_intent == "getInformation":
            st.session_state.search_intent = True
            return intent_funcs[predicted_intent](query)
        else:        
            st.session_state.search_intent = False
            return intent_funcs[predicted_intent]()

# Streamlit
st.title("StayMate")

# loading resources
if "initialised" not in st.session_state:
    with st.spinner("Getting things ready..."):
        #ontology
        onto = get_ontology("inferred_property_rental.owl").load()
        st.session_state.onto = onto
        #model
        st.session_state.model = joblib.load('model.pkl')
        st.session_state.vectorizer = joblib.load('vectorizer.pkl')
        # checking if intent is search properties
        st.session_state.search_intent = False
        #session slots
        st.session_state.slots = {
            "city": None,
            "date_from": None,
            "date_to": None,
            "amenities": [],
            "property_type": None,
            "guest_rating": None,
            "booking_policy": None,
            "min_price": 0,
            "max_price": None,
        }
        st.session_state.user_slots = {
            "city": None,
            "dates": None,
            "amenities": "",
            "property_type": None,
            "guest_rating": None,
            "booking_policy": None,
            "price_range": None
        }
        #ready
        st.session_state.initialised = True

# init resources
onto = st.session_state.get("onto", None)
model = st.session_state.get("model")
vectorizer = st.session_state.get("vectorizer")
slots = st.session_state.slots
user_slots = st.session_state.user_slots

# Initialize chats
if "chat_history" not in st.session_state:
    st.info(
        """
        💬 **Need help getting started?**

        Try asking things like:
        
        "Show me places in Granada for August 1-3"  
        "I need an apartment for under 200 pounds a night"  
        "Can I see all your locations?"

        Start chatting when you're ready! ☺️
        """
    )
    st.session_state.chat_history = []

# Input and interaction
user_input = st.chat_input("Looking for a place to stay?")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    response = getIntent(user_input)
    st.session_state.chat_history.append(("bot", response))

# Display chat
for index, (role, msg) in enumerate(st.session_state.chat_history):
    with st.chat_message(role):
        if role == "bot" and index == len(st.session_state.chat_history) - 1 and any(st.session_state.user_slots.values()) and st.session_state.search_intent == True:
            with st.expander("Filters & Options ⚙️"):
                if st.button("New Chat 🧹"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
                for key, value in st.session_state.user_slots.items():
                    if value:
                        st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")
        if role == 'bot':
            st.markdown(msg)
        else:
            st.write(msg)         