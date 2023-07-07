import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

## config
st.set_page_config(layout="wide")

## constans
GRAPH_MAX = 19
GRAPH_MIN = 0
GEN_MAX = 9
GEN_MIN = 0

## cache html data
@st.cache
def get_html_files(html_dir_name):
    intial = {}
    optimized = {}

    # get intial graph html files
    for graph_no in range(20):
        path = "./files/" + html_dir_name + "/layout0-" + str(graph_no) + ".html"
        with open(path) as f:
            intial[graph_no] = f.read()

        path = "./files/" + html_dir_name + "/layout9-" + str(graph_no) + ".html"
        with open(path) as f:
            optimized[graph_no] = f.read()

    return intial, optimized


intial_graph_d, optimized_graph_d = get_html_files("html_files")


def each_graph():
    ## sidebar
    with st.sidebar:
        graph_no = st.number_input(
            "グラフ番号", step=1, min_value=GRAPH_MIN, max_value=GRAPH_MAX
        )
        gen_no = st.number_input("世代番号", step=1, min_value=GEN_MIN, max_value=GEN_MAX)

        st.markdown("----")
        st.write("グラフ番号: ", graph_no)
        st.write("世代番号: ", gen_no)

    ## main contents
    st.title("Graph Viewer")

    path = "./files/html_files/layout" + str(gen_no) + "-" + str(graph_no) + ".html"
    with open(path) as f:
        _html = f.read()
        components.html(_html, height=800, width=800)


def compare():
    ## sidebar
    with st.sidebar:
        graph_no = st.number_input(
            "グラフ番号", step=1, min_value=GRAPH_MIN, max_value=GRAPH_MAX
        )

        st.markdown("----")
        st.write("グラフ番号: ", graph_no)

    ## main contents
    st.title("Compare Graph")

    image = Image.open("pareto.png")
    st.image(image, caption="Pareto Front")

    # Initialグラフ と Optimizedグラフを横並びで表示
    left, right = st.columns(2)

    with left:
        st.markdown("### Initial Graph")
        components.html(intial_graph_d[graph_no], height=800, width=800)

    with right:
        st.markdown("### Optimized Graph")
        components.html(optimized_graph_d[graph_no], height=800, width=800)


def show_all(graph_d, isOptimized):
    if isOptimized:
        st.title("Show All Optimized Graph")
    else:
        st.title("Show All Initial Graph")

    graphs = [None for i in range(20)]

    # 2つずつ横並びで表示
    for i in range(0, 19, 2):
        graphs[i], graphs[i + 1] = st.columns(2)

        with graphs[i]:
            st.markdown("### Graph" + str(i))
            components.html(graph_d[i], height=800, width=800)

        with graphs[i + 1]:
            st.markdown("### Graph" + str(i + 1))
            components.html(graph_d[i + 1], height=800, width=800)


def main():
    st.sidebar.markdown("## ページ切り替え")
    ## menuを選択
    menu = st.sidebar.radio(
        "メニュー", ("each graph", "compare", "show all (optim)", "show all (init)")
    )

    # --- page振り分け
    if menu == "each graph":
        each_graph()
    elif menu == "compare":
        compare()
    elif menu == "show all":
        show_all(optimized_graph_d, isOptimized=True)
    else:
        show_all(intial_graph_d, isOptimized=False)


## メイン
main()
