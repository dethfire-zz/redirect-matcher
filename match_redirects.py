import streamlit as st
import pandas as pd
from polyfuzz import PolyFuzz
import base64

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p class="big-font">URL Redirect Matcher</p>
<b>Directions: </b></ br><ol>
<li>Upload CSV of ScreamingFrog crawl or URL list (URL column labeled 'Address')</li>
<li>Upload CSV of 404s from GSC (URL column named 'URL')</li>
<li>Would not recommend with over 10k URLs (very slow)</li>
</ol>
""", unsafe_allow_html=True)

domain_path = st.text_input('Your root domain path','ex https://www.domain.com')

get_broken = st.file_uploader("Upload 404 CSV File",type=['csv'])
get_current = st.file_uploader("Upload Crawl CSV File",type=['csv'])

if get_broken is not None and get_current is not None:
    
    st.write("Processing, please wait... :sunglasses:")
    
    broken = pd.read_csv(get_broken)
    blogs = pd.read_csv(get_current)
    
    broken_list = broken["URL"].tolist()
    broken_list = [sub.replace('https://www.rayallen.com', '') for sub in broken_list]
    
    blogs_list = blogs["Address"].tolist()
    blogs_list = [sub.replace('https://www.rayallen.com', '') for sub in blogs_list]
    
    model = PolyFuzz("EditDistance")
    model.match(broken_list, blogs_list)
    
    df = model.get_matches()
    
    df = df.sort_values(by='Similarity', ascending=False)
    df["Similarity"] = df["Similarity"].round(3)

    index_names = df[ df['Similarity'] < .857 ].index
    amt_dropped = len(index_names)
    df.drop(index_names, inplace = True)

    df["To"] = "https://www.rayallen.com" + df["To"]
    
    def get_csv_download_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="redirect-matches.csv">-- Download CSV Redirect File --</a>'
    
    st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
    st.dataframe(df)
    
st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [Rocket Clicks](https://www.rocketclicks.com), [importSEM](https://importsem.com) and [Physics Forums](https://www.physicsforums.com)')
