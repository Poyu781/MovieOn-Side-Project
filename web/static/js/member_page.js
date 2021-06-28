// const ratingSubmit = document.querySelector(".ratingSubmit")

// const numberOfRating = document.querySelector(" numberOfRating")
const reviewedSection= document.querySelector(".movies__block")

const userId = document.querySelector(".user").id



function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie__information");
    node.setAttribute("id", movieObject.internal_id)
    
    let img = movieObject.img;
    let internal_rating = movieObject.rating
    let internal_id = movieObject.internal
    let title_name = movieObject.main_taiwan_name

    let htmlText = `
    <a class="movie-ranking" href="movie/${internal_id}">
  <img src=${img} />
  <div class="movie__info">
    <h4>${title_name}</h4>
    <h5>${internal_rating}<span>分</span></h5>
  </div>
  </a>
`;
    node.innerHTML = htmlText;
    nodeDiv.appendChild(node);
}


function main(url,node) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            let dataArray = datalist; //I will get a list of dict
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            for (let i = 0; i < Math.min(num,6); i++) {
                renderMovies(dataArray[i], node);
            }

        });
    }
main(`api/member/${userId}/movies/`,reviewedSection)
const similartiySection = document.querySelector(".similarity")
function getSimilarity(url,nodeDiv){
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            if (datalist.message === "not enough"){
                nodeDiv.innerHTML = '<h2 style="margin: 0 auto;"> 資料量不足，需要評分超過 10 部影片才能顯示</h2>'
            }
            else{
            let dataArray = datalist
            let imdb_sim = Math.round(dataArray.imdb*100,2);
            let douban_sim = Math.round(dataArray.douban*100,2)
            let tomato_sim = Math.round(dataArray.tomato*100,2)

            let htmlText = `
            <div class="similarity__block">
            <p>與 Imdb 相似程度</p>
            <div class="progress" data-percent="${imdb_sim}%" style="--percent: ${imdb_sim}px; --background: #f3ce13"></div>
          </div>
          <div class="similarity__block">
            <p>與 豆瓣 相似程度</p>
            <div class="progress" data-percent="${douban_sim}%" style="--percent: ${douban_sim}px; --background: #08CE14"></div>
          </div>
          <div class="similarity__block">
            <p>與 爛番茄觀眾 相似程度</p>
            <div class="progress" data-percent="${tomato_sim}%" style="--percent: ${tomato_sim}px; --background: #F70006"></div>
          </div>
        `;
        nodeDiv.innerHTML = htmlText;
            }
})}
getSimilarity(`api/member/${userId}/similarity/`,similartiySection)

function renderView(movieObject, nodeDiv) {
    node = document.createElement("div")
    let img = movieObject.img;
    let internal_id = movieObject.internal
    let title_name = movieObject.main_taiwan_name

    let htmlText = `
    <a class="movie-card" href="movie/${internal_id}">
    <img src=${img} />
    <div class="movie__info">
      <h4>${title_name}</h4>
    </div>
     
    </a>
`;
    node.innerHTML = htmlText ;
    nodeDiv.appendChild(node)
}
viewedSection = document.querySelector(".viewed__block")
function getViewedMovie(url,nodeDiv){
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {
            let num = datalist.length;
            for (let i = 0; i < num; i++) {
                renderView(datalist[i], nodeDiv);
            }
})}
getViewedMovie(`api/member/${userId}/viewed_movie/`,viewedSection)
