# OpenAPI Specification

## Info
- **Title:** 
- **Version:** 0.0.0

## Paths

### `/api/course/courses/`
#### GET
- **Operation ID:** `course_courses_list`
- **Description:** View for managing course APIs.
- **Parameters:**
  - `tags` (query, string): Comma-separated list of IDs to filter
- **Tags:** `course`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - Type: `array`
          - Items:
            - `$ref`: `#/components/schemas/Course`

#### POST
- **Operation ID:** `course_courses_create`
- **Description:** View for managing course APIs.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
  - **Required:** `true`
- **Security:** `tokenAuth`
- **Responses:**
  - `201`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/CourseDetail`

### `/api/course/courses/{id}/`
#### GET
- **Operation ID:** `course_courses_retrieve`
- **Description:** View for managing course APIs.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this course.
- **Tags:** `course`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/CourseDetail`

#### PUT
- **Operation ID:** `course_courses_update`
- **Description:** View for managing course APIs.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this course.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseDetailRequest`
  - **Required:** `true`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/CourseDetail`

#### PATCH
- **Operation ID:** `course_courses_partial_update`
- **Description:** View for managing course APIs.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this course.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedCourseDetailRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedCourseDetailRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedCourseDetailRequest`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/CourseDetail`

#### DELETE
- **Operation ID:** `course_courses_destroy`
- **Description:** View for managing course APIs.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this course.
- **Tags:** `course`
- **Security:** `tokenAuth`
- **Responses:**
  - `204`:
    - **Description:** No response body

### `/api/course/courses/{id}/upload-image/`
#### POST
- **Operation ID:** `course_courses_upload_image_create`
- **Description:** Upload an image to a course.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this course.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseImageRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseImageRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/CourseImageRequest`
  - **Required:** `true`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/CourseImage`

### `/api/course/tags/`
#### GET
- **Operation ID:** `course_tags_list`
- **Description:** Manage tags in the database.
- **Parameters:**
  - `assigned_only` (query, integer): Filter by items assigned to courses.
- **Tags:** `course`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - Type: `array`
          - Items:
            - `$ref`: `#/components/schemas/Tag`

### `/api/course/tags/{id}/`
#### PUT
- **Operation ID:** `course_tags_update`
- **Description:** Manage tags in the database.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this tag.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/TagRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/TagRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/TagRequest`
  - **Required:** `true`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/Tag`

#### PATCH
- **Operation ID:** `course_tags_partial_update`
- **Description:** Manage tags in the database.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this tag.
- **Tags:** `course`
- **Request Body:**
  - **Content:**
    - `application/json`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedTagRequest`
    - `application/x-www-form-urlencoded`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedTagRequest`
    - `multipart/form-data`:
      - **Schema:**
        - `$ref`: `#/components/schemas/PatchedTagRequest`
- **Security:** `tokenAuth`
- **Responses:**
  - `200`:
    - **Content:**
      - `application/json`:
        - **Schema:**
          - `$ref`: `#/components/schemas/Tag`

#### DELETE
- **Operation ID:** `course_tags_destroy`
- **Description:** Manage tags in the database.
- **Parameters:**
  - `id` (path, integer): A unique integer value identifying this tag.
- **Tags:** `course`
- **Security:** `tokenAuth`
- **Responses:**
  - `204`:
    - **Description:** No response body

### `/api/schema/`
#### GET
- **Operation ID:** `schema_retrieve`
- **Description:** OpenApi3 schema for this API. Format can be selected via content negotiation.
  - YAML: `application/vnd.oai.openapi`
  - JSON: `application/vnd.oai.openapi+json`
- **Parameters:**
  - `format` (query, string): Format of the schema
    - **Enum:** `json`, `yaml`
  - `lang` (query, string): Language of the schema
    - **Enum:** `af`, `ar`, `ar-dz`, `ast`, `az`, `be`, `bg`, `bn`, `br`, `bs`, `ca`, `cs`, `cy`, `da`, `de`, `dsb`, `el`, `en`, `en-au`, `en-gb`, `eo`, `es`, `es-ar`, `es-co`, `es-mx`, `es-ni`, `es-ve`, `et`, `eu
