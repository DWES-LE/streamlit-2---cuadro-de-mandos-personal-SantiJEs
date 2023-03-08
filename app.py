import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
from bokeh.plotting import figure

st.set_page_config(layout="wide")

@st.cache_data
def load_data(URL):
    data = pd.read_csv(URL)
    data.index = pd.date_range(start="1/1/18", periods=len(data), freq="D")
    return data

df = load_data('penguins.csv')

plot_types = (
    "Dispersión",
    "Histograma",
    "Barras",
    "Lineal",
    "Dispersión 3D",
)
libs = (
    "Matplotlib",
    "Seaborn",
    "Plotly Express",
    "Altair",
    "Pandas Matplotlib",
    "Bokeh",
)

st.title("📊 Datos sobre pingüinos del archipielago Palmer (la Antártida) 🐧")
st.header("Con varios tipos de gráficas de distintas librerías populares de python")

with st.sidebar:
    st.title("Elige el tipo de gráfica y algún filtro para el conjunto de datos")
    chart_type = st.selectbox("Elige el tipo de gráfica", plot_types)
    genero = st.selectbox("Sexo", ("Ambos", "Macho", "Hembra"))

if genero == 'Hembra':
    genero = 'female'
elif genero == 'Macho':
    genero = 'male'
else:
    genero = None

if genero != None:
    df = df.query("sex == @genero")

def matplotlib_plot(chart_type: str, df):  
    fig, ax = plt.subplots()
    if chart_type == "Dispersión":
        with st.echo():
            df["color"] = df["species"].replace(
                {"Adelie": 1, "Chinstrap": 2, "Gentoo": 3}
            )
            ax.scatter(x=df["body_mass_g"], y=df["flipper_length_mm"], c=df["color"])
            plt.title("Longitud de las aletas según el peso corporal")
            plt.xlabel("Peso corporal (g)")
            plt.ylabel("Longitud de las aletas (mm)")
    elif chart_type == "Histograma":
        with st.echo():
            plt.title("Especimenes observados de cada especie")
            ax.hist(df["species"])
            plt.xlabel("Especies")
            plt.ylabel("Número de especimenes")
    elif chart_type == "Barras":
        with st.echo():
            df_plt = df.groupby("species", dropna=False).mean().reset_index()
            ax.bar(x=df_plt["species"], height=df_plt["body_mass_g"])
            plt.title("Peso corporal medio de cada especie")
            plt.xlabel("Especies")
            plt.ylabel("Peso corporal (g)")
    elif chart_type == "Lineal":
        with st.echo():
            ax.plot(df.index, df["body_mass_g"])
            plt.title("Peso corporal a lo largo del tiempo")
            plt.ylabel("Peso corporal (g)")
    elif chart_type == "Dispersión 3D":
        ax = fig.add_subplot(projection="3d")
        with st.echo():
            df["color"] = df["species"].replace(
                {"Adelie": 1, "Chinstrap": 2, "Gentoo": 3}
            )
            df["numIsland"] = df["island"].replace(
                {"Torgersen": 1, "Biscoe": 2, "Dream": 3}
            )
            ax.scatter3D(
                xs=df["body_mass_g"],
                ys=df["flipper_length_mm"],
                zs=df["numIsland"],
                c=df["color"],
            )
            ax.set_xlabel("Peso corporal (g)")
            ax.set_ylabel("Longitud de las aletas (mm)")
            ax.set_zlabel("Islas (1=Torgersen, 2=Biscoe, 3=Dream)")
            plt.title("Longitud de las aletas según el peso corporal en cada isla")
    return fig

def sns_plot(chart_type: str, df):
    fig, ax = plt.subplots()
    if chart_type == "Dispersión":
        with st.echo():
            sns.scatterplot(
                data=df,
                x="body_mass_g",
                y="flipper_length_mm",
                hue="species",
            )
            plt.title("Longitud de las aletas según el peso corporal de cada especie")
    elif chart_type == "Histograma":
        with st.echo():
            sns.histplot(data=df, x="species")
            plt.title("Especimenes observados de cada especie")
    elif chart_type == "Barras":
        with st.echo():
            sns.barplot(data=df, x="species", y="body_mass_g")
            plt.title("Peso corporal medio de cada especie")
    # elif chart_type == "Boxplot":
    #     with st.echo():
    #         sns.boxplot(data=df)
    #         plt.title("Bill Depth Observations")
    elif chart_type == "Lineal":
        with st.echo():
            sns.lineplot(data=df, x=df.index, y="body_mass_g")
            plt.title("Peso corporal a lo largo del tiempo")
    elif chart_type == "Dispersión 3D":
        st.write("Seaborn no hace gráficas en 3D ☹️. Aquí hay otra dispersión 2D.")
        sns.scatterplot(data=df, x="body_mass_g", y="flipper_length_mm", hue="island")
        plt.title("Longitud de las aletas según el peso corporal en cada isla")
    return fig

def plotly_plot(chart_type: str, df):
    if chart_type == "Dispersión":
        with st.echo():
            fig = px.scatter(
                data_frame=df,
                x="body_mass_g",
                y="flipper_length_mm",
                color="species",
                title="Longitud de las aletas según el peso corporal",
            )
    elif chart_type == "Histograma":
        with st.echo():
            fig = px.histogram(
                data_frame=df,
                x="species",
                title="Especimenes observados de cada especie",
            )
    elif chart_type == "Barras":
        with st.echo():
            fig = px.histogram(
                data_frame=df,
                x="species",
                y="body_mass_g",
                title="Peso corporal medio de cada especie",
                histfunc="avg",
            )
            # by default shows stacked bar chart (sum) with individual hover values
    # elif chart_type == "Boxplot":
    #     with st.echo():
    #         fig = px.box(data_frame=df, x="species", y="bill_depth_mm")
    elif chart_type == "Lineal":
        with st.echo():
            fig = px.line(
                data_frame=df,
                x=df.index,
                y="body_mass_g",
                title="Peso corporal a lo largo del tiempo",
            )
    elif chart_type == "Dispersión 3D":
        with st.echo():
            fig = px.scatter_3d(
                data_frame=df,
                x="body_mass_g",
                y="flipper_length_mm",
                z="island",
                color="species",
                title="Gráfica 3D de longitud de las aletas según el peso corporal en cada isla interactiva",
            )

    return fig


def altair_plot(chart_type: str, df):
    if chart_type == "Dispersión":
        with st.echo():
            fig = (
                alt.Chart(
                    df,
                    title="Longitud de las aletas según el peso corporal",
                )
                .mark_point()
                .encode(x="body_mass_g", y="flipper_length_mm", color="species")
                .interactive()
            )
    elif chart_type == "Histograma":
        with st.echo():
            fig = (
                alt.Chart(df, title="Especimenes observados de cada especie")
                .mark_bar()
                .encode(alt.X("species", bin=False), y="count()")
                .interactive()
            )
    elif chart_type == "Barras":
        with st.echo():
            fig = (
                alt.Chart(
                    df.groupby("species", dropna=False).mean().reset_index(),
                    title="Peso corporal medio de cada especie",
                )
                .mark_bar()
                .encode(x="species", y="body_mass_g")
                .interactive()
            )
    # elif chart_type == "Boxplot":
    #     with st.echo():
    #         fig = (
    #             alt.Chart(df).mark_boxplot().encode(x="species:O", y="bill_depth_mm:Q")
    #         )
    elif chart_type == "Lineal":
        with st.echo():
            fig = (
                alt.Chart(df.reset_index(), title="Peso corporal a lo largo del tiempo")
                .mark_line()
                .encode(x="index:T", y="body_mass_g:Q")
                .interactive()
            )
    elif chart_type == "Dispersión 3D":
        st.write("Altair no hace gráficas en 3D ☹️. Aquí hay otra dispersión 2D.")
        fig = (
            alt.Chart(df, title="Longitud de las aletas según el peso corporal en cada isla")
            .mark_point()
            .encode(x="body_mass_g", y="flipper_length_mm", color="island")
            .interactive()
        )
    return fig


def pd_plot(chart_type: str, df):
    fig, ax = plt.subplots()
    if chart_type == "Dispersión":
        with st.echo():
            df["color"] = df["species"].replace(
                {"Adelie": "blue", "Chinstrap": "orange", "Gentoo": "green"}
            )
            ax_save = df.plot(
                kind="scatter",
                x="body_mass_g",
                y="flipper_length_mm",
                c="color",
                ax=ax,
                title="Longitud de las aletas según el peso corporal",
            )
    elif chart_type == "Histograma":
        with st.echo():
            df["numEspecie"] = df["species"].replace(
                {"Adelie": 1, "Chinstrap": 2, "Gentoo": 3}
            )
            ax_save = df["numEspecie"].plot(
                kind="hist", ax=ax, title="Especimenes observados de cada especie"
            )
            plt.xlabel("Especies")
    elif chart_type == "Barras":
        with st.echo():
            ax_save = (
                df.groupby("species", dropna=False)
                .mean()
                .plot(
                    kind="bar",
                    y="body_mass_g",
                    title="Peso corporal medio de cada especie",
                    ax=ax,
                )
            )
            plt.ylabel("Peso corporal (g)")
    # elif chart_type == "Boxplot":
    #     with st.echo():
    #         ax_save = df.plot(kind="box", ax=ax)
    elif chart_type == "Lineal":
        with st.echo():
            ax_save = df.plot(kind="line", use_index=True, y="body_mass_g", ax=ax)
            plt.title("Peso corporal a lo largo del tiempo")
            plt.ylabel("Peso corporal (g)")
    elif chart_type == "Dispersión 3D":
        st.write("Pandas no hace gráficas en 3D ☹️. Aquí hay otra dispersión 2D.")
        ax_save = df.plot(kind="scatter", x="body_mass_g", y="flipper_length_mm", ax=ax)
        plt.title("Longitud de las aletas según el peso corporal")
    return fig


def bokeh_plot(chart_type: str, df):
    if chart_type == "Dispersión":
        with st.echo():
            df["color"] = df["species"].replace(
                {"Adelie": "blue", "Chinstrap": "orange", "Gentoo": "green"}
            )
            fig = figure(title="Longitud de las aletas según el peso corporal")
            fig.circle(source=df, x="body_mass_g", y="flipper_length_mm", color="color")
    elif chart_type == "Histograma":
        with st.echo():
            df["numEspecie"] = df["species"].replace(
                {"Adelie": 1, "Chinstrap": 2, "Gentoo": 3}
            )
            hist, edges = np.histogram(df["numEspecie"].dropna(), bins=3)
            fig = figure(title="Especimenes observados de cada especie")
            fig.quad(
                top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white"
            )
    elif chart_type == "Barras":
        with st.echo():
            fig = figure(
                title="Peso corporal medio de cada especie",
                x_range=["Gentoo", "Chinstrap", "Adelie"],
            )

            fig.vbar(
                source=df.groupby("species", dropna=False).mean(),
                x="species",
                top="body_mass_g",
                width=0.8,
            )

    elif chart_type == "Lineal":
        with st.echo():
            fig = figure(title="Peso corporal a lo largo del tiempo", x_axis_type="datetime")
            fig.line(source=df.reset_index(), x="index", y="body_mass_g")

    elif chart_type == "Dispersión 3D":
        st.write("Bokeh no hace gráficas en 3D ☹️. Aquí hay otra dispersión 2D.")
        df["color"] = df["species"].replace(
            {"Adelie": "blue", "Chinstrap": "orange", "Gentoo": "green"}
        )
        fig = figure(title="Longitud de las aletas según el peso corporal")
        fig.circle(source=df, x="body_mass_g", y="flipper_length_mm", color="color")

    return fig


def show_plot(kind: str):
    st.header(kind)
    if kind == "Matplotlib":
        plot = matplotlib_plot(chart_type, df)
        st.pyplot(plot)      
    elif kind == "Seaborn":
        plot = sns_plot(chart_type, df)
        st.pyplot(plot)
    elif kind == "Plotly Express":
        plot = plotly_plot(chart_type, df)
        st.plotly_chart(plot, use_container_width=True)
    elif kind == "Altair":
        plot = altair_plot(chart_type, df)
        st.altair_chart(plot, use_container_width=True)
    elif kind == "Pandas Matplotlib":
        plot = pd_plot(chart_type, df)
        st.pyplot(plot)
    elif kind == "Bokeh":
        plot = bokeh_plot(chart_type, df)
        st.bokeh_chart(plot, use_container_width=True)


for lib in libs:
    show_plot(kind=lib)
