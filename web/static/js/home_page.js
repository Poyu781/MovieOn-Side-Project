const itemsSection = document.querySelector(".home__content");
function renderMovies(movieObject, nodeDiv) {
    let node = document.createElement("div");
    node.classList.add("movie");
    node.setAttribute("id", movieObject.imdb.imdb_id)
    
    let img = movieObject.imdb.image;
    let title = movieObject.imdb.movie_title;
    let imdb_rating = movieObject.imdb_rating
    let path = movieObject.imdb.imdb_id
    let rotten_audience_rating = movieObject.audience_rating
    let rotten_tomator_rating = movieObject.tomator_rating
    let douban_rating = movieObject.douban_rating
    let htmlText = `
        <a class="movie" href= movie/${path}>
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


function main(url,offsetNum) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist["results"]; //I will get a list of dict
            console.log(dataArray)
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            for (let i = 0; i < num; i++) {
                renderMovies(dataArray[i], itemsSection);
            }

        });
}
offsetNum = 0
main('/api/rating/?limit=12&offset=0',offsetNum)

showMoreButton = document.querySelector(".button__more")
showMoreButton.addEventListener("click",()=>{
    offsetNum += 12
    main(`/api/rating/?limit=12&offset=${offsetNum}`,offsetNum)
})