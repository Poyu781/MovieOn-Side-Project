// const ratingSubmit = document.querySelector(".ratingSubmit")

// const numberOfRating = document.querySelector(" numberOfRating")
const movieDetail = document.querySelector(".movie__information")
const movieSection= document.querySelector(".movie__section")

let str = window.location.pathname;
let internalId = str.match(/[0-9].*/)[0];
console.log(internalId);


function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie__information");
    node.setAttribute("id", movieObject.internal_id)
    
    let img = movieObject.img;
    let cnTitle = movieObject.main_taiwan_name;
    let engTitle = movieObject.main_original_name;
    let theaterDate = movieObject.date_in_theater
    let runTime = movieObject.runtime_minutes
    let imdbId = movieObject.imdb_id
    let doubanId = movieObject.douban_id
    let tomatoId = movieObject.rotten_tomato_id
    let imdbRating = movieObject.rating
    let imdbCount = movieObject.rating_count
    let rottenAudienceRating = movieObject.audience_rating
    let rottenAudienceCount = movieObject.audience_rating_amount
    let rottenTomatorRating = movieObject.tomator_rating
    let rottenTomatorCount = movieObject.tomator_rating_amount
    let doubanRating = movieObject.avg_rating
    let doubanRatingCount = movieObject.total_rating_amount
    let director_list = movieObject.director_list
    let actor_list = movieObject.actor_list
    let feature_list = movieObject.feature_list
    let htmlText = `
    <img src=${img}  />
    <div class="movie__detail">
      <h2>${cnTitle}</h2>
      <h2>${engTitle}</h2>
      <ul>
        <li>導演：${director_list}</li>
        <li>演員：${actor_list}</li>
        <li>片長：${runTime} 分鐘</li>
        <li>上映日期：${theaterDate}</li>
        <li>類型：${feature_list}</li>
      </ul>
      <div class="movie__ranking">
      <div>
          <a href="https://www.imdb.com/title/${imdbId}">
        <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png"/>
          </a>
        <p>${imdbRating}（共 ${imdbCount} 筆評分）</p>
      </div>
      <div>
      <a href="https://movie.douban.com/subject/${doubanId}">
        <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg"/>
      </a>
        <p>${doubanRating}（共 ${doubanRatingCount} 筆評分）</p>
      </div>
      <div>
        <a href="https://www.rottentomatoes.com/m/${tomatoId}">
        <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png"/>
        </a>
        <p>  觀眾評分：${rottenAudienceRating}（共 ${rottenAudienceCount} 筆評分）
             影評評分：${rottenTomatorRating}（共 ${rottenTomatorCount} 筆評分）</p>
      </div>
    </div>
    <div class="movie__intro">
    ${movieObject.chinese_description}
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
            console.log(dataArray[0])
            renderMovies(dataArray[0], movieSection);
            let nodeRecommend = document.createElement("div");
nodeRecommend.classList.add("movie__recommend");
nodeRecommend.innerHTML = `
<a class="movie" href="movie/tt8096832">
<img src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg" />
<div class="movie__info">
  <h3>綠色奇蹟</h3>
  <div class="rank">
    <div>
      <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/imdb.png"/>
      <p>6.3</p>
    </div>
    <div>
      <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/douban.jpg"/>
      <p>6.90</p>
    </div>
    <div>
      <img src="https://stylishforjimmy.s3-ap-northeast-1.amazonaws.com/tomato.png"/>
      <p>80</p>
    </div>
  </div>
</div>
</a>

`
movieSection.appendChild(nodeRecommend)
        });
    }
main(`/api/detail/${internalId}`)

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
const path = document.location['pathname'];

let userRating = document.querySelector("#rating").innerHTML;

if (userRating != ""){
    console.log(userRating)
    document.querySelector(`#star${userRating}`).checked=true
}
const ratingSection = document.querySelector(".rating")
ratingSection.addEventListener("change",(e)=>{
    let ratingValue = document.querySelector('input[name="rating"]:checked').value
    let data = {"rating":ratingValue, "imdb_id":internalId}
    // numberOfRating.innerHTML = `Choose Rating :${ratingValue}`
    console.log(data)
    fetch("/rating",{
        method: "POST",
        mode: 'same-origin',
        
        body : JSON.stringify(data),
        headers : {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
    })

        .then((res)=>{

            return res.json()
        })
        .catch((error) => {
            window.location.href = `/signin?next=${path}`;
            console.log('Error:', error)
        })
        .then((json)=>{
            console.log(json)
        })
    })

