# =============================================================================
# Load modules
# =============================================================================
import streamlit as st
import pandas as pd
import matplotlib as plt

font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 5}
plt.rc('font', **font)


st.set_page_config(layout="wide")

# Title
st.title("Visualisation of option implied quantiles and expectiles")
st.markdown('This project is joint work with [Arthur Böök](https://de.linkedin.com/in/arthurbook), [Juan Imbet](https://jfimbett.github.io), '
            '[Martin Reinke](https://www.en.bank.bwl.uni-muenchen.de/team/mitarbeiter/reinke/index.html) and [Carlo Sala](https://www.esade.edu/faculty/carlo.sala).')
st.markdown("")
st.markdown('This app allows you to see per day the estimation result for our proposed method (BIRS)'
            ' and two other methods proposed in the literature.')
st.markdown('Please note that the paper is currently work in progress. Comments welcome.')
st.markdown("")
st.markdown("Option data on 'Weeklys' are downloaded from OptionMetrics.")


chck = st.sidebar.checkbox("Use your theme colours on graphs", value=True) # get colours for graphs

# get colors from theme config file, or set the colours to altair standards
if chck:
    primary_clr = st.get_option("theme.primaryColor")
    txt_clr = st.get_option("theme.textColor")
    # I want 3 colours to graph, so this is a red that matches the theme:
    second_clr = "#d87c7c"
else:
    primary_clr = '#4c78a8'
    second_clr = '#f58517'
    txt_clr = '#e45756'






# =============================================================================
# Load results data for Böök and Sala
# =============================================================================
filenameBookSala = 'results_bookSala.parquet.gzip'
root = './data/'
location = root + filenameBookSala
results_bookSala = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_bookSala = results_bookSala.groupby(['date'])
# Extract as list, for easier access
groupList_bookSala  = list(g_date_expiry_bookSala)

# =============================================================================
# Load results data for Jackwerth (2004)
# =============================================================================
filename_jackwerth = 'results_jackwerth.parquet.gzip'
root = './data/'
location = root + filename_jackwerth
results_jackwerth = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_jackwerth = results_jackwerth.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_jackwerth  = list(g_date_expiry_jackwerth)


# =============================================================================
# Load results data for Bondarenko (2003)
# =============================================================================
filename_bondarenko = 'results_bondarenko.parquet.gzip'
root = './data/'
location = root + filename_bondarenko
results_bondarenko = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_bondarenko = results_bondarenko.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_bondarenko  = list(g_date_expiry_bondarenko)

# =============================================================================
# Load filtered data and no violations of LCS (2003)
# =============================================================================

# LCS
filename_lcs = 'results_lcs.parquet.gzip'
root = './data/'
location = root + filename_lcs
results_lcs = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_lcs = results_lcs.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_lcs  = list(g_date_expiry_lcs)


# Arbitrage violation
filename_arbViolations = 'results_arbViolations.parquet.gzip'
root = './data/'
location = root + filename_arbViolations
results_arbViolations = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_arbViolations = results_arbViolations.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_arbViolations  = list(g_date_expiry_arbViolations)


# =============================================================================
# Visulize results data
# =============================================================================

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((4,3))

with row1_1:
    st.title("Estimated option implied quantiles and expectiles")
    date_selected = st.slider("Select date in the sample", 0, len(g_date_expiry_jackwerth)-1)

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
row3_1, row3_2, row3_3, row3_4 = st.columns((1,1,1,1))
row4_1, row4_2, row4_3, row4_4 = st.columns((1,1,1,1))


date = '0'
days = [str(x) for x in range(len(g_date_expiry_jackwerth))]

# =============================================================================
# Define helper functions
# =============================================================================
# Filter data by date selected

def get_dataset(groupList, date, dataset_name):
    
    date_num = int(date)
    raw_data = ['lcs', 'arbViolations']
    
    if any(x in dataset_name for x in raw_data):
        results = groupList[date_num][1][['K/F', 'strike_price', 'forward_price', 'callprice','iv_raw']]
    
    else:
        results = groupList[date_num][1][['K/F', 'strike', 'forward', 'prices', 'vols', 'QAlpha', 'QPDF', 'EAlpha','EPDF']]
    
    
    resultsSort =  results.sort_values('K/F')
    
    resultsSort = resultsSort.set_index('K/F')
    
    return resultsSort


# Get data from selection
source_bookSala = get_dataset(groupList_bookSala, date_selected, 'bookSala')
source_jackwerth = get_dataset(groupList_jackwerth, date_selected, 'jackwerth')
source_bondarenko = get_dataset(groupList_bondarenko, date_selected, 'bondarenko')

# =============================================================================
# Our approach BIRS
# =============================================================================
with row2_1:
    st.write("Our approach (BIRS)")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bookSala['prices'],'k', linewidth=1)
    ax.set_ylim(0, 200)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 
    #st.line_chart(source_bookSala['prices'])

with row2_2:
    st.write("Quantile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bookSala['QAlpha'],'k', linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig)
    #st.line_chart(source_bookSala['QAlpha'])

with row2_3:
    st.write("Expectile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bookSala['EAlpha'],'k', linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig)
    
    #st.line_chart(source_bookSala['EAlpha'])


# =============================================================================
# Jackwerth (2004)
# =============================================================================
with row3_1:
    st.write("Jackwerth (2004)")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_jackwerth['prices'],'k', linewidth=1)
    ax.set_ylim(0, 200)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 
    #st.line_chart(source_jackwerth['prices'])

with row3_2:
    st.write("Quantile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_jackwerth['QAlpha'],'k', linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 
    # st.line_chart(source_jackwerth['QAlpha'])


with row3_3:
    st.write("Expectile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_jackwerth['EAlpha'], 'k',linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig)
    #st.line_chart(source_jackwerth['EAlpha'])


# =============================================================================
# Bondarenko (2003)
# =============================================================================
with row4_1:
    st.write("Bondarenko (2003)")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bondarenko['prices'],'k', linewidth=1)
    ax.set_ylim(0, 200)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 

with row4_2:
    st.write("Quantile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bondarenko['QAlpha'],'k', linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 

with row4_3:
    st.write("Expectile-CDF")
    fig, ax = plt.pyplot.subplots(figsize=(1.25, 1.25))
    ax.plot(source_bondarenko['EAlpha'],'k', linewidth=1)
    ax.set_ylim(0, 1)
    ax.set_xlim(0.7, 1.2)
    ax.set_xlabel("Forward moneyness (K/F)")
    ax.grid(alpha = 0.3)
    st.pyplot(fig) 
    #st.line_chart(source_bondarenko['EAlpha'])







