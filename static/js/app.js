document.addEventListener('DOMContentLoaded', () => {
    // Product Form Handling
    const productForm = document.getElementById('productForm');
    const productList = document.getElementById('productList');

    if (productForm) {
        productForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const formData = {
                name: document.getElementById('name').value,
                category: document.getElementById('category').value,
            };

            fetch('/product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Product added successfully!") {
                    loadProducts();
                    productForm.reset();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });

        function loadProducts() {
            fetch('/products')
                .then(response => response.json())
                .then(products => {
                    productList.innerHTML = '';
                    products.forEach(product => {
                        const li = document.createElement('li');
                        li.textContent = `${product.name} - ${product.category} (Introduced: ${product.introduce_date})`;
                        productList.appendChild(li);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        loadProducts();
    }

    // Purchase Form Handling
    const purchaseForm = document.getElementById('purchaseForm');
    const purchaseList = document.getElementById('purchaseList');

    if (purchaseForm) {
        purchaseForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const formData = {
                product_id: document.getElementById('product').value,
                purchase_quantity: document.getElementById('quantity').value,
                purchase_rate: document.getElementById('rate').value
            };

            fetch('/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Purchase entry added successfully and stock updated!") {
                    loadPurchases();
                    purchaseForm.reset();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });

        function loadPurchases() {
            fetch('/purchases')
                .then(response => response.json())
                .then(purchases => {
                    purchaseList.innerHTML = '';
                    purchases.forEach(purchase => {
                        const li = document.createElement('li');
                        li.textContent = `Product ID: ${purchase.product_id} - Quantity: ${purchase.purchase_quantity} (Rate: ${purchase.purchase_rate}, Amount: ${purchase.purchase_amount}, Date: ${purchase.purchase_date})`;
                        purchaseList.appendChild(li);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        loadPurchases();
    }

    // Stock Form Handling
    const stockForm = document.getElementById('stockForm');
    const stockList = document.getElementById('stockList');

    if (stockForm) {
        stockForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const formData = {
                product_id: document.getElementById('product').value,
                product_quantity: document.getElementById('quantity').value
            };

            fetch('/stock', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Stock entry added successfully!") {
                    loadStocks();
                    stockForm.reset();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });

        function loadStocks() {
            fetch('/stocks')
                .then(response => response.json())
                .then(stocks => {
                    stockList.innerHTML = '';
                    stocks.forEach(stock => {
                        const li = document.createElement('li');
                        li.textContent = `Product ID: ${stock.product_id} - Quantity: ${stock.product_quantity} (Last Update: ${stock.last_update_date})`;
                        stockList.appendChild(li);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        loadStocks();
    }

    // Sales Form Handling
    const salesForm = document.getElementById('salesForm');
    const salesList = document.getElementById('salesList');

    if (salesForm) {
        salesForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const formData = {
                product_id: document.getElementById('product').value,
                sales_quantity: document.getElementById('quantity').value,
                sales_rate: document.getElementById('rate').value
            };

            fetch('/sale', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Sale entry added successfully and stock updated!") {
                    loadSales();
                    salesForm.reset();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });

        function loadSales() {
            fetch('/sales')
                .then(response => response.json())
                .then(sales => {
                    salesList.innerHTML = '';
                    sales.forEach(sale => {
                        const li = document.createElement('li');
                        li.textContent = `Product ID: ${sale.product_id} - Quantity: ${sale.sales_quantity} (Rate: ${sale.sales_rate}, Amount: ${sale.sales_amount}, Date: ${sale.sales_date})`;
                        salesList.appendChild(li);
                    });
                })
                .catch(error => console.error('Error:', error));
        }

        loadSales();
    }
});

function showPopup(title, message) {
    // Update the popup content
    document.getElementById('actionModalLabel').innerText = title;
    document.querySelector('#actionModal .modal-body p').innerText = message;

    // Show the popup
    var actionModal = new bootstrap.Modal(document.getElementById('actionModal'));
    actionModal.show();
}


// function showPopup(title, message) {
//     const popupModal = new bootstrap.Modal(document.getElementById('genericPopup'));
//     document.getElementById('popupTitle').innerText = title;
//     document.getElementById('popupMessage').innerText = message;
//     popupModal.show();
// }