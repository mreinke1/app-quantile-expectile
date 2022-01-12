# =============================================================================
# Load modules
# =============================================================================
import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(layout="wide")

# Title
st.title("Visualisation of option implied quantiles and expectiles")
st.markdown('This project is joint work with [Arthur Böök](https://de.linkedin.com/in/arthurbook), [Juan Imbet](https://jfimbett.github.io), '
            '[Martin Reinke](https://www.en.bank.bwl.uni-muenchen.de/team/mitarbeiter/reinke/index.html) and [Carlo Sala](https://www.esade.edu/faculty/carlo.sala).'
            ' The Github repository is available [here](https://github.com/mreinke1/app-quantile-expectile)')
st.markdown('This app allows you to see per day the estimation result for our proposed method (BIRS) to extract option implied quantiles and expectiles.'
            ' We benchmark our approach with two other methods proposed in the literature.'
            ' Please note that the paper is currently work in progress. Comments welcome.')
st.markdown("")
st.markdown("We use short term options so called 'weeklys' on the S&P 500 traded on the CBOE and downloaded from OptionMetrics."
            " Statistically, quantiles and expectiles share many similar properties but differ substantially in one aspect."
            " While quantiles determines the value of X such that the probability of the variable being less than or equal to "
            " that value equals a given level. Expectiles are linked to the properties of the expectation"
            " of the random variable X, conditional on X being into the tail of the distribution.")

st.subheader("Option implied quantiles")
st.latex(r'''
         \alpha_{t,T}(K_{i}) = e^{r(T-t)} \left[ \lambda \dfrac{C_{t,T}(K_{i+1})-C_{t,T}(K_{i})}{K_{i+1}- K_{i}} + \left(1- \lambda \right) \dfrac{C_{t,T}(K_{i})-C_{t,T}(K_{i-1})}{K_{i}- K_{i-1}} \right] +1\\
         ''')
st.subheader("Option implied expectiles")
st.latex(r'''
         \theta_{t,T}(K_{i}) = \dfrac{P_{t,T}(K_{i})}{P_{t,T}(K_{i}) + C_{t,T}(K_{i})}
         ''')

# =============================================================================
# Load results data for our approach (BIRS)
# =============================================================================
filenamebirs = 'results_birs_noLCS.parquet.gzip'
root = './data/'
location = root + filenamebirs
results_birs = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_birs = results_birs.groupby(['date'])
# Extract as list, for easier access
groupList_birs  = list(g_date_expiry_birs)

# =============================================================================
# Load results data for Jackwerth (2004)
# =============================================================================
filename_jackwerth = 'results_jackwerth_noLCS.parquet.gzip'
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
filename_bondarenko = 'results_bondarenko_noLCS.parquet.gzip'
root = './data/'
location = root + filename_bondarenko
results_bondarenko = pd.read_parquet(location)

# Group Panel by date and expiry
g_date_expiry_bondarenko = results_bondarenko.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_bondarenko  = list(g_date_expiry_bondarenko)

# =============================================================================
# Load data after filter
# =============================================================================
filename_lcs = 'OptionsData_after_filter.parquet.gzip'
root = './data/'
location = root + filename_lcs
data_after_filter = pd.read_parquet(location)

# Group panel by date and expiry
g_date_expiry_data = data_after_filter.groupby(['date','exdate'])
# Extract as list, for easier access
groupList_data  = list(g_date_expiry_data)


# =============================================================================
# Visulize results data
# =============================================================================

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((4,3))

with row1_1:
    st.header("Estimation of option implied quantiles and expectiles")
    date_selected = st.slider("Select date in the sample", 0, len(g_date_expiry_jackwerth)-1)

# LAYING OUT THE MIDDLE SECTION OF THE APP
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
    
    #resultsSort = resultsSort.set_index('K/F')
    
    return resultsSort


def get_raw_data(groupList, date):
    
    date_num = int(date)
    
    results = groupList[date_num][1][['K/F', 'strike_price', 'forward_price', 'callprice']]
    
    resultsSort =  results.sort_values('K/F')
        
    return resultsSort

#%% Get data
# Raw data
source_data = get_raw_data(groupList_data, date_selected)

# Get data from selection
source_birs = get_dataset(groupList_birs, date_selected, 'birs')
source_jackwerth = get_dataset(groupList_jackwerth, date_selected, 'jackwerth')
source_bondarenko = get_dataset(groupList_bondarenko, date_selected, 'bondarenko')

# =============================================================================
# Our approach BIRS
# =============================================================================

with row2_1:
    st.write("Our approach (BIRS)")
    base = alt.Chart(source_data).mark_circle(clip = True, color = '#7D3C98').encode(
        alt.X("K/F", scale=alt.Scale(domain=[0.7,1.2])),
        alt.Y("callprice", scale=alt.Scale(domain=[0, 200])),
        #alt.Color(legend=alt.Legend(values=['Observed market prices'])),
        alt.Color('Legend',
                  scale=alt.Scale(range=['#7d3c98'], domain=['callprice']),
                  legend=alt.Legend(values=['Total']))
)
    c = alt.Chart(source_birs[['K/F','prices']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('prices', scale=alt.Scale(domain=[0, 200]), axis=alt.Axis(title='in USD')) #
        )
    
    st.altair_chart(base + c , use_container_width=True)
    

with row2_2:
    st.write("Quantile-CDF")
    c = alt.Chart(source_birs[['K/F','QAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('QAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)

with row2_3:
    st.write("Expectile-CDF")
    c = alt.Chart(source_birs[['K/F','EAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('EAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)

# =============================================================================
# Jackwerth (2004)
# =============================================================================
with row3_1:
    st.write("Jackwerth (2004)")
    
    base = alt.Chart(source_data).mark_circle(clip = True, color = '#7D3C98').encode(
        alt.X("K/F", scale=alt.Scale(domain=[0.7,1.2])),
        alt.Y("callprice", scale=alt.Scale(domain=[0, 200]))
)
    
    c = alt.Chart(source_bondarenko[['K/F','prices']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('prices', scale=alt.Scale(domain=[0, 200]), axis=alt.Axis(title='in USD'))
        )
    st.altair_chart(base + c, use_container_width=True)

with row3_2:
    st.write("Quantile-CDF")
    c = alt.Chart(source_jackwerth[['K/F','QAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('QAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)


with row3_3:
    st.write("Expectile-CDF")
    c = alt.Chart(source_jackwerth[['K/F','EAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('EAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)

# =============================================================================
# Bondarenko (2003)
# =============================================================================
with row4_1:
    st.write("Bondarenko (2003)")
    
    base = alt.Chart(source_data).mark_circle(clip=True, color = '#7D3C98').encode(
        alt.X("K/F", scale=alt.Scale(domain=[0.7,1.2])),
        alt.Y("callprice", scale=alt.Scale(domain=[0, 200]))
)
    
    c = alt.Chart(source_bondarenko[['K/F','prices']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('prices', scale=alt.Scale(domain=[0, 200]), axis=alt.Axis(title='in USD'))
        )
    
    st.altair_chart(base + c, use_container_width=True)

with row4_2:
    st.write("Quantile-CDF")
    c = alt.Chart(source_bondarenko[['K/F','QAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('QAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)
    
with row4_3:
    st.write("Expectile-CDF")
    c = alt.Chart(source_bondarenko[['K/F','EAlpha']]).mark_line(clip=True).encode(
        alt.X('K/F', scale=alt.Scale(domain=[0.7,1.2]), axis=alt.Axis(title='Forward moneyness K/F')), 
        alt.Y('EAlpha', scale=alt.Scale(domain=[0, 1.1]), axis=alt.Axis(title=''))
        )
    st.altair_chart(c, use_container_width=True)


# List of references
st.header("References")
st.markdown('Bondarenko, O. (2003). Estimation of risk-neutral densities using positive convolution approximation. Journal of Econometrics, 116(1-2), 85-112 ')
st.markdown('Jackwerth, J. C. (2004). Option-Implied Risk-Neutral Distributions and Risk Aversion, Research Foundation of AIMR, Charlottesville, VA, ISBN 0-943205-66-2.')

