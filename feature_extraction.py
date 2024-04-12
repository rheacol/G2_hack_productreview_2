import pandas as pd
import re
from collections import Counter


df = pd.read_excel('survey_responses.xlsx')


def preprocess_text(text):
    words = re.findall(r'\b\w+\b', str(text).lower())
    return words


def extract_features(tokens):
    features = []
    
    if 'public' in tokens and 'validation' in tokens:
        features.append('Public validation')
    
    if 'pipeline' in tokens:
        features.append('Pipeline building')
    if 'showcase' in tokens and 'vendors' in tokens:
        features.append('Showcasing vendors')
    if 'smart' in tokens and 'grid' in tokens:
        features.append('Smart grid feature')
    if 'brand' in tokens and 'new' in tokens:
        features.append('Building brand in new space')
    if 'end' in tokens and 'service' in tokens:
        features.append('End-to-end service')
    if 'continuous' in tokens and 'flow' in tokens:
        features.append('Continuous flow of reviews')
    if 'proactive' in tokens and 'outreach' in tokens:
        features.append('Proactive outreach for reviews')
    if 'automation' in tokens:
        features.append('Automation of review process')
    if 'high' in tokens and 'rate' in tokens:
        features.append('High rate of reviews and referrals')

   
    if 'visibility' in tokens or 'exposure' in tokens:
        features.append('Visibility improvement')
    if 'success' in tokens and 'facilitates' in tokens:
        features.append('Success facilitation')
    if 'automated' in tokens or 'automation' in tokens:
        features.append('Automation implementation')
    if 'integration' in tokens or 'integrating' in tokens:
        features.append('Integration capability')

    return ', '.join(features) 


def extract_drawbacks(review):
    
    
    features = []
    if "dislike" in review:
        features.append("No specific dislikes mentioned")
    if "incentive" in review:
        features.append("Lack of willingness to review without incentives")
    if "LinkedIn integration" in review:
        features.append("Positive experience with LinkedIn integration")
    if "integration" in review:
        features.append("Need for integration with other systems")
    if "feature-light" in review:
        features.append("Product is feature-light")
    if "early product" in review:
        features.append("Early-stage product with limited features")

    return ', '.join(features) 
    
    


def extract_benefits(text):
    features = []
    
    keywords = {
        'brand building': ['brand', 'business', 'exposure', 'inbound leads'],
        'review scaling': ['scale', 'review processes', 'encourage', 'promoters', 'share experience'],
        'advocacy recognition': ['recognize', 'value', 'advocates', 'automated', 'time saving', 'cost efficient'],
        'review gathering': ['garner', 'reviews', 'advocately', 'workflow', 'unobtrusive', 'impact'],
        'advocacy program': ['advocacy', 'impact', 'price point'],
        'marketing efficiency': ['online reputation', 'benefits', 'star ratings', 'adwords ads', 'digital marketing', 'effort saving'],
        'customer feedback': ['awesome reviews', 'refer', 'friends'],
        'review outreach': ['reach out', 'NPS promoters', 'app marketplaces']
    }
   
    for feature, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in text:
                features.append(feature)
                break  
    return ', '.join(features) 
def extract_recommendations(text):
    recommendations = []

    keywords = {
        'best practices': ['best practices', 'learn', 'leverage'],
        'growth': ['growth', 'integrate'],
        'quality': ['quality', 'deliver'],
        'reviews gathering': ['reviews gathering', 'set up', 'platform setup']
        
    }
    
    for feature, keywords_list in keywords.items():
        for keyword in keywords_list:
            if keyword in text:
                recommendations.append(feature)
                break  
    return ', '.join(recommendations) 


df['Features'] = df['attributes.comment_answers.love.value'].apply(lambda x: extract_features(preprocess_text(x)))
df['Drawbacks'] = df['attributes.comment_answers.hate.value'].apply(lambda x: extract_drawbacks(preprocess_text(x)))
df['Recommendations'] = df['attributes.comment_answers.recommendations.value'].apply(lambda x: extract_recommendations(preprocess_text(x)))
df['Benefits'] = df['attributes.comment_answers.benefits.value'].apply(lambda x: extract_benefits(preprocess_text(x)))


df.to_excel('updated_excel_with_features.xlsx', index=False)
for index, row in df.iterrows():
    features = row['Features']
    drawbacks = row['Drawbacks']
    recommendations = row['Recommendations']
    benefits = row['Benefits']

    
    verified_user = row['attributes.verified_current_user']
    review_source = row['attributes.review_source']
    organic_review = 'organic' in review_source.lower()
    partner_review = row['attributes.is_business_partner']
    
    
    rating_count = df[(df['attributes.star_rating'] == row['attributes.star_rating']) & 
                      (df['attributes.verified_current_user'] == True)].shape[0]
    
    if (verified_user and organic_review) or (not partner_review and not organic_review and rating_count >= 5):
        print(f"Summary for Review #{index + 1}:")
        print(f"Features: {features}")
        print(f"Drawbacks: {drawbacks}")
        print(f"Recommendations: {recommendations}")
        print(f"Benefits: {benefits}")
        print()
