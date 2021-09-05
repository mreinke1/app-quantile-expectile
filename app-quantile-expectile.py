# =============================================================================
# Load modules
# =============================================================================
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Title
st.title("Visualisation of option implied quantiles and expectiles")
st.markdown('Web App by Martin Reinke ([reinke@lmu.de](https://github.com/mreinke1))')
st.markdown("")
st.markdown("This app allows you to see the estimation result for different methods"
            " employed to estimated option implied quantiles and expectiles."
            "The paper is currently work in progress by XXX.")

with st.expander("Data Information"):
    st.markdown("Weekly option data from OptionMetrics.")


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
row1_1, row1_2 = st.columns((5,3))

with row1_1:
    st.title("Estimated option implied quantile and expectiles")
    date_selected = st.slider("Select date in the sample", 0, len(g_date_expiry_jackwerth))

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_0, row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
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
    
    return resultsSort


# Get data from selection
source_bookSala = get_dataset(groupList_bookSala, date_selected, 'bookSala')
source_jackwerth = get_dataset(groupList_jackwerth, date_selected, 'jackwerth')
source_bondarenko = get_dataset(groupList_bondarenko, date_selected, 'bondarenko')



# =============================================================================
# Our approach BIRS
# =============================================================================
with row2_0:
    st.write("BIRS (our approach)")
    
with row2_1:
    #st.write("BIRS (our approach)")
    st.line_chart(source_bookSala['QAlpha'])

with row2_2:
    st.write("")
    st.line_chart(source_bookSala['EAlpha'])


# =============================================================================
# Jackwerth (2004)
# =============================================================================
with row3_1:
    st.write("Jackwerth (2004)")
    st.line_chart(source_jackwerth['QAlpha'])

with row3_2:
    st.write("Jackwerth (2004)")
    st.line_chart(source_jackwerth['EAlpha'])


# =============================================================================
# Bondarenko (2003)
# =============================================================================
with row4_1:
    st.write("Bondarenko (2003)")
    st.line_chart(source_bondarenko['QAlpha'])

with row4_2:
    st.write("Bondarenko (2003)")
    st.line_chart(source_bondarenko['EAlpha'])




# with row2_2:
#     st.write("**La Guardia Airport**")
#     map(data, la_guardia[0],la_guardia[1], zoom_level)

# with row2_3:
#     st.write("**JFK Airport**")
#     map(data, jfk[0],jfk[1], zoom_level)

# with row2_4:
#     st.write("**Newark Airport**")
#     map(data, newark[0],newark[1], zoom_level)






