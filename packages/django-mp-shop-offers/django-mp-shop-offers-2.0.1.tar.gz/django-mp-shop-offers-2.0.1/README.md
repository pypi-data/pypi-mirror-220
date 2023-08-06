# MP-Shop | Offers

### Installation:

1) Install using PIP:
```
pip install django-mp-shop-offers
```

2) Add `'offers'` to `INSTALLED_APPS`.

3) Add `path('offers/', include('offers.urls'))` to `urlpatterns`.

4) Add `offers/offers.js` to js files list.

### Template example:

```
<a href="javascript:void(0);" data-role="show-price-offer-modal">
    Send offer
</a>
```

```
<script>
    $(window).load(function() {

        new PriceOfferModal({
            url: '{% url 'offers:modal' object.id %}',
            $target: $('[data-role="show-price-offer-modal"]')
        });

    });
</script>
```

### Requirements:
* django >= 2.0.6
* python >= 3.5.2
