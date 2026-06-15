# Business Insights Report

Generated at: 2026-06-15 03:47:50.252446


Warranty vs resale value correlation: 0.3540

Crack severity vs resale value correlation: -0.3249

Condition score vs resale value correlation: 0.4835


Categories retaining value longest:

                  avg_price_retention_pct  avg_age_days  avg_condition_score  count
product_category                                                                   
Furniture                       38.385656   1200.342380            53.575157    958
Microwaves                      33.572523   1180.822688            55.721068   1049
Televisions                     32.086189   1154.556202            55.883333   1032
Washing Machines                31.729504   1158.963489            53.409939    986
Refrigerators                   31.523261   1189.340909            53.007335    968


Categories depreciating fastest:

                  avg_price_retention_pct  avg_age_days  avg_condition_score  count
product_category                                                                   
Tablets                         29.912680   1154.495876            54.348969    970
Headphones                      29.766668   1177.735830            53.035830    988
Smart Watches                   29.597044   1194.439379            53.385451   1031
Laptops                         29.446969   1184.057277            54.345540   1065
Mobile Phones                   28.846307   1213.385100            54.002833    953


Impact of condition score on price:

condition_bucket
Poor          7658.788053
Fair         13788.779693
Good         19920.824679
Very Good    29370.889121
Excellent    52995.621485
Name: resale_price, dtype: float64