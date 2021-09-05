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
row1_1, row1_2 = st.columns((4,3))

with row1_1:
    st.title("Estimated option implied quantile and expectiles")
    date_selected = st.slider("Select date in the sample", 0, len(g_date_expiry_jackwerth))


date = '0'
days = [str(x) for x in range(len(g_date_expiry_jackwerth))]









