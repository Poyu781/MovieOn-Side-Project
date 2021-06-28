const loadNode = document.querySelector(".loader__wrapper")
const itemsSection = document.querySelector(".home__content");
const loadingGif = document.querySelector(".loader__wrapper")
// const searchButton = document.querySelector(".button__search")
let query = window.location.search;
function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie");
    node.setAttribute("id", movieObject.internal)
    
    let img = movieObject.img;
    let title = movieObject.main_taiwan_name;
    let imdb_rating = movieObject.imdb_rating
    let path = movieObject.internal
    let rotten_audience_rating = movieObject.audience_rating
    let rotten_tomator_rating = movieObject.tomator_rating
    let douban_rating = movieObject.douban_rating
    let htmlText = `
        <a class="movie" href= movie/${path} target="_blank">
        <img src=${img}>
        <div class="movie__info">
            <h3>${title}</h3>
            <div class="rank">
                <div>
                    <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png">
                    <p>${imdb_rating}</p>
                </div>
                <div>
                    <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg">
                    <p>${douban_rating}</p>
                </div>
                <div>
                    <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png">
                    <p>${rotten_audience_rating}</p>
                </div>
            </div>
        </div>
`;
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
}


function main(url) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist; //I will get a list of dict

            
            let num = dataArray.length;
            if (num == 0){
                itemsSection.innerHTML ="<h3 style='color:white'>查無相關結果</h3>"
            }
// Math.ceil(offsetNum/4);
            loadNode.style.display = "none"
            for (let i = 0; i < num; i++) {
                renderMovies(dataArray[i], itemsSection);
            }

        });
}

main(`/api/search${query}`)
