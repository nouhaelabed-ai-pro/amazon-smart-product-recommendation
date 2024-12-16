document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const recommendationsModal = document.getElementById('recommendationsModal');
    
    // Initialize Bootstrap modal
    const modal = new bootstrap.Modal(recommendationsModal);
    
    let searchTimeout;
    const searchCache = new Map();

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.classList.add('d-none');
                return;
            }

            // Check cache first
            if (searchCache.has(query)) {
                displaySearchResults(searchCache.get(query));
                return;
            }

            searchTimeout = setTimeout(() => {
                // Show loading state
                searchResults.innerHTML = '<div class="search-result-item"><i class="fas fa-spinner fa-spin me-2"></i>Searching...</div>';
                searchResults.classList.remove('d-none');

                fetch(`/search?query=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        // Cache the results
                        searchCache.set(query, data);
                        displaySearchResults(data);
                    })
                    .catch(error => {
                        console.error('Search error:', error);
                        searchResults.innerHTML = '<div class="search-result-item text-danger"><i class="fas fa-exclamation-circle me-2"></i>Error fetching results</div>';
                    });
            }, 300);
        });
    }

    // Get recommendations functionality
    document.querySelectorAll('.get-recommendations').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const recommendationsList = document.getElementById('recommendationsList');
            
            // Show loading state in modal
            recommendationsList.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p class="mt-2">Loading recommendations...</p></div>';
            modal.show();

            fetch(`/api/similar-products/${productId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    displayRecommendations(data);
                })
                .catch(error => {
                    console.error('Recommendations error:', error);
                    recommendationsList.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-circle me-2"></i>
                            Error loading recommendations
                        </div>
                    `;
                });
        });
    });

    function displaySearchResults(data) {
        if (!Array.isArray(data)) {
            console.error('Invalid search results:', data);
            searchResults.innerHTML = '<div class="search-result-item text-danger"><i class="fas fa-exclamation-circle me-2"></i>Invalid search results</div>';
            return;
        }

        searchResults.innerHTML = '';
        
        if (data.length === 0) {
            searchResults.innerHTML = '<div class="search-result-item">No products found</div>';
            searchResults.classList.remove('d-none');
            return;
        }

        data.forEach(product => {
            const div = document.createElement('div');
            div.className = 'search-result-item';
            
            // Create rating stars
            const rating = Math.round(product.rating);
            const stars = Array(5).fill('').map((_, index) => 
                `<i class="fa${index < rating ? 's' : 'r'} fa-star"></i>`
            ).join('');

            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">${product.product_name}</h6>
                        <div class="text-muted small">${product.category.split('|')[0]}</div>
                        <div class="rating text-warning mb-1">${stars}</div>
                    </div>
                    <div class="text-end">
                        <div class="price">₹${product.discounted_price.toFixed(2)}</div>
                        <div class="small text-muted">${product.rating_count} ratings</div>
                    </div>
                </div>
            `;

            div.addEventListener('click', () => {
                const recommendationsList = document.getElementById('recommendationsList');
                recommendationsList.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p class="mt-2">Loading recommendations...</p></div>';
                modal.show();

                fetch(`/api/similar-products/${product.product_id}`)
                    .then(response => response.json())
                    .then(data => displayRecommendations(data))
                    .catch(error => {
                        console.error('Error:', error);
                        recommendationsList.innerHTML = '<div class="alert alert-danger">Error loading recommendations</div>';
                    });
            });

            searchResults.appendChild(div);
        });

        searchResults.classList.remove('d-none');
    }

    function displayRecommendations(products) {
        const recommendationsList = document.getElementById('recommendationsList');
        
        if (!Array.isArray(products)) {
            recommendationsList.innerHTML = '<div class="alert alert-danger">Invalid recommendations data</div>';
            return;
        }

        if (products.length === 0) {
            recommendationsList.innerHTML = '<div class="alert alert-info">No similar products found</div>';
            return;
        }

        recommendationsList.innerHTML = `
            <div class="row">
                ${products.map(product => `
                    <div class="col-md-6 mb-3">
                        <div class="card h-100">
                            <div class="card-body">
                                <h6 class="card-title">${product['Product Name']}</h6>
                                <p class="card-text small text-muted">${product.Category}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="price">₹${product.Price.toFixed(2)}</div>
                                    <div class="rating text-warning">
                                        ${Array(Math.round(product.Rating)).fill('').map(() => '<i class="fas fa-star"></i>').join('')}
                                    </div>
                                </div>
                                <div class="mt-2 small text-muted">
                                    Similarity: ${(product['Similarity Score'] * 100).toFixed(1)}%
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Hide search results when clicking outside
    document.addEventListener('click', function(e) {
        if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.classList.add('d-none');
        }
    });
});
