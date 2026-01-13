# Video Format Training Dataset 

# **Video Format Training Dataset Construction Process**

**Overview**

This document describes the systematic process of constructing a **high-quality training dataset** for video format analysis and reward modeling. The dataset aims to capture diverse video formats across different engagement levels for training AI models to understand and predict video performance.

**Current Dataset Statistics (as of 2025-12-30):**

- **286 formats** with human-verified reference videos

- **1,696 total videos** (5.9 videos per format on average)

- **View range:** 0 to 38.6M views (avg: 1.08M views)

---

## **Dataset Construction Pipeline**

### **Phase 1: Format Discovery & Hypothesis Generation**

**Objective:** Identify distinct video formats from successful TikTok content creators.

**Process:**

1. **Creator Selection**: Analyze top-performing TikTok creators from various niches

2. **Video Clustering**: Use AI (Gemini Vision API) to identify unique format patterns within each creator's content

3. **Hypothesis Creation**: Generate format hypotheses describing:

- Visual style (e.g., "POV from driver's seat", "Before/After split screen")

- Content structure (e.g., "Story time with text overlay")

- Engagement patterns (e.g., "Tutorial with step-by-step captions")

**Output:** `content_format_training` table with format definitions

---

### **Phase 2: Reference Video Collection**

**Objective:** Find diverse, high-quality reference videos for each format using multi-tier search strategies.

#### **2.1 Diversified Search Strategy**

To ensure representation across ALL engagement levels (not just viral hits), we implemented a **view-tier-based search approach**:

**Search Methods:**

1. **Original Search (19.5% of videos):**

- Direct semantic search using format hypothesis

- Typically finds high-engagement videos (confirmation bias toward viral content)

2. **Diversified Search (80.5% of videos):**

   - **Dashboard-based search**: Query low-view creator dashboards (e.g., 100-1K followers)

   - **Days-back temporal search**: Search recent posts (last 7/30/90 days) to capture new/rising formats

   - **Tier-specific quotas**: Deliberately collect videos from each view tier

   - **JINA embedding similarity**: Match videos to format hypothesis using semantic similarity

---

### **Phase 3: AI Verification**

**Objective:** Automatically verify that reference videos truly match the format hypothesis.

**AI Verification Process:**

1. **Visual Analysis**: Gemini Vision API analyzes video frames + metadata

2. **Match Scoring**: AI evaluates alignment between video and format hypothesis

3. **Reasoning Generation**: AI provides explanation for verification decision

4. **Binary Decision**: `is_verified = True/False`

**Filtering Criteria:**

- Semantic similarity score (JINA embedding) > threshold

- AI verification reasoning indicates strong format match

- Video metadata quality (has valid URL, duration, engagement metrics)

**Output:** Videos marked with `is_verified = True` in `format_reference_training` table

---

### **Phase 4: Human Verification (Critical Quality Control)**

**Objective:** Human reviewers validate AI decisions to ensure dataset quality.

**Human Review Workflow:**

1. **Review Interface**: Human reviewers watch videos and compare to format hypothesis

2. **Three-way Decision:**

   - correct: Video accurately represents the format (98.6% of current dataset)

   - incorrect: Video does NOT match the format (filtered out in export)

3. **Metadata Captured:**

- `human_verified_status`: correct/incorrect/skip

- `human_verified_by`: Reviewer identifier

- `human_verified_at`: Timestamp of review

**Quality Assurance:**

- **Inter-rater reliability**: Multiple reviewers for subset of videos

- **Annotation guidelines**: Clear criteria for format matching

- **Feedback loop**: Incorrect videos help improve AI verification prompts

**Current Status:** 98.6% of videos marked as 'correct' (1,672/1,696 videos)

---

### **Phase 5: Dataset  & Training Preparation**

#### **5.1 Data Structure**

Each exported record contains:

**Format-Level Data:**

```json
{
  // Identifiers
  "content_id": "7423856...",
  "platform": "tiktok",
  
  // Content metadata
  "title": "When your coworker...",
  "description": "#fyp #office #relatable",
  "duration": 45.2,
  "created_at": "2025-11-15T10:30:00",
  
  // Engagement metrics
  "views_count": 1245678,
  "likes_count": 98765,
  "comments_count": 3456,
  "shares_count": 2345,
  "save_count": 890,
  
  // Performance indicators
  "views_to_follower_ratio": 15.7,
  "is_10x_content": true,
  
  // Creator info
  "creator_id": "user123",
  "creator_name": "@office_life",
  "creator_followers": 79345,
  
  // AI analysis
  "text_overlay": "When your manager asks...",
  "voice_over": "Original audio",
  
  // Training metadata
  "rank": 1,
  "jina_similarity_score": 0.87,
  "verification_reasoning": "Strong POV perspective...",
  "search_strategy": "diversified",
  "view_tier": "100K-1M",
  
  // Human verification
  "human_verified_status": "correct",
  "human_verified_by": "reviewer_001",
  "human_verified_at": "2025-12-20T14:30:00"
}
````

  

---

## **Dataset Quality Metrics**

**👥 Creator Follower Distribution**

- Range: 0 → 55.2M followers

- Average: 129.8K followers

**👥 Video View Distribution**

# ** Creator Wise Training Dataset Construction Process**

## **Dataset Construction Pipeline**

### Datasource 1: Jobright Creator Overview

### Datasource2: Turbolearn Creator Overview

### Datasource3: Studyfetch Creator Overview

## Data Structure

## Data Quality Metrics

