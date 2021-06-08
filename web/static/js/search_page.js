const itemsSection = document.querySelector(".home__content");
const searchButton = document.querySelector(".button__search")
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


function main(url) {
    fetch(url)
        .then((response) => {
            return response.json();
        })
        .then((datalist) => {

            let dataArray = datalist; //I will get a list of dict
            console.log(dataArray)
            let num = dataArray.length;
// Math.ceil(offsetNum/4);
            for (let i = 0; i < num; i++) {
                renderMovies(dataArray[i], itemsSection);
            }

        });
}
let offsetNum = 0
main('/api/movie')
let feature_id = false
// showMoreButton = document.querySelector(".button__more")
// showMoreButton.addEventListener("click",()=>{
//     offsetNum += 20
//     console.log(feature_id)
//     if (feature_id){
//         main(`/api/movie/?start=${offsetNum}&feature=${feature_id}`)
//     }
//     else{
//         main(`/api/movie/?start=${offsetNum}`)
//     }
// })

// for (let i = 1; i < 4; i++) {
//     let elem = document.querySelector('.tag');
//     console.log(1)
//     elem.addEventListener('click', function() {
//         feature_id = 12
//         offsetNum = 0
//         itemsSection.innerHTML = ""
        
//         main(`/api/movie/?start=${offsetNum}&feature=${feature_id}`)
//     });
// }
let elem = document.querySelector('.search__section');

elem.addEventListener('click', function(e) {
    // console.log(e.target.id)
    if (e.target.type == "radio"){
    console.log(e.target)
    let feature_id = e.target.id
    console.log("d",feature_id)
    let offsetNum = 0
    itemsSection.innerHTML = ""
    if (feature_id == "a"){
    main('/api/movie')
    
}
    else if (feature_id){
        main(`/api/movie/?start=${offsetNum}&feature=${feature_id}`)
    }
    }
});

searchButton.addEventListener("click",()=>{
    let search_value = document.querySelector("input[type='text']").value
    itemsSection.innerHTML = ""
    showMoreButton.style.display = "none";
    main(`/api/search?query=${search_value}`)
})