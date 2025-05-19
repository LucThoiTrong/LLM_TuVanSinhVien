import json
from openai import AzureOpenAI

# Azure OpenAI configuration
endpoint = "https://trongopenai.openai.azure.com/"
deployment = "gpt-35-turbo"
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2024-12-01-preview"

# Initialize client
client = None

# Dữ liệu chuyên ngành
data = [
    {
        "chuyen_nganh": "Công nghệ Phần mềm",
        "mo_ta_chung": "Đào tạo các kỹ năng cần thiết để phát triển, thiết kế, kiểm thử và quản lý các sản phẩm phần mềm đáp ứng nhu cầu thực tiễn.",
        "mo_ta_chi_tiet_hon": "Chuyên ngành Công nghệ Phần mềm tập trung vào việc trang bị cho sinh viên kiến thức toàn diện về quy trình phát triển phần mềm, từ khâu thu thập yêu cầu, phân tích, thiết kế hệ thống, lập trình, kiểm thử, triển khai cho đến bảo trì và quản lý dự án. Sinh viên sẽ được học cách áp dụng các phương pháp luận tiên tiến, công cụ hiện đại và các mẫu thiết kế phổ biến để xây dựng những ứng dụng phần mềm chất lượng cao, có khả năng mở rộng và dễ bảo trì, phục vụ đa dạng các lĩnh vực từ ứng dụng web, di động đến các hệ thống doanh nghiệp phức tạp.",
        "mon_hoc_tieu_bieu": ["Nhập môn lập trình", "Cấu trúc dữ liệu và giải thuật", "Lập trình hướng đối tượng", "Cơ sở dữ liệu", "Kỹ thuật phần mềm (Software Engineering Principles)", "Phân tích và thiết kế phần mềm", "Lập trình Web (Frontend & Backend)", "Lập trình ứng dụng di động", "Kiểm thử phần mềm (Software Testing & QA)", "Quản lý dự án phần mềm", "Kiến trúc phần mềm", "An toàn thông tin ứng dụng", "Phát triển game (Tùy chọn)"],
        "ky_nang_can_thiet": {"ky_nang_ky_thuat": ["Thành thạo ít nhất một ngôn ngữ lập trình (ví dụ: Java, Python, JavaScript, C#)", "Hiểu biết về cấu trúc dữ liệu và giải thuật", "Kiến thức về cơ sở dữ liệu (SQL, NoSQL)", "Kỹ năng phát triển web (HTML, CSS, JavaScript, frameworks như React, Angular, Vue.js, Node.js, Django, Spring)", "Kỹ năng phát triển ứng dụng di động (Swift, Kotlin, React Native, Flutter)", "Kiến thức về quy trình phát triển phần mềm (Agile, Scrum, Waterfall)", "Kỹ năng sử dụng hệ thống quản lý phiên bản (Git, SVN)", "Kỹ năng kiểm thử phần mềm (Manual & Automation)", "Hiểu biết về kiến trúc phần mềm và các mẫu thiết kế", "Kiến thức cơ bản về mạng máy tính và bảo mật"], "ky_nang_mem": ["Tư duy logic và giải quyết vấn đề", "Kỹ năng làm việc nhóm", "Kỹ năng giao tiếp (bằng lời và văn bản)", "Khả năng tự học và cập nhật công nghệ mới", "Sự tỉ mỉ và chú ý đến chi tiết", "Kỹ năng quản lý thời gian và tổ chức công việc", "Tư duy phản biện", "Sáng tạo"]},
        "cong_cu_va_cong_nghe_pho_bien": {"ngon_ngu_lap_trinh": ["Java", "Python", "JavaScript", "C#", "PHP", "Ruby", "Swift", "Kotlin", "Go", "TypeScript"], "frameworks_thu_vien": ["React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Spring Boot", ".NET", "Ruby on Rails", "jQuery", "Bootstrap"], "co_so_du_lieu": ["MySQL", "PostgreSQL", "MongoDB", "SQL Server", "Oracle", "SQLite", "Firebase Realtime Database", "Redis"], "cong_cu_phat_trien_quan_ly": ["Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Slack", "Docker", "Kubernetes", "Jenkins", "Visual Studio Code", "IntelliJ IDEA", "Eclipse", "Android Studio", "Xcode"], "nen_tang_dam_may": ["Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Heroku"]},
        "co_hoi_nghe_nghiep": ["Kỹ sư phần mềm (Software Engineer/Developer)", "Lập trình viên Full-stack", "Lập trình viên Frontend", "Lập trình viên Backend", "Lập trình viên ứng dụng di động (Mobile Developer - iOS, Android)", "Kỹ sư kiểm thử phần mềm (QA/QC Engineer, Tester)", "Kỹ sư DevOps", "Kiến trúc sư phần mềm (Software Architect)", "Quản lý dự án phần mềm (Project Manager)", "Chuyên viên phân tích nghiệp vụ (Business Analyst)", "Kỹ sư phát triển game (Game Developer)", "Chuyên viên hỗ trợ kỹ thuật phần mềm"],
        "muc_luong_khoi_diem": "12-25 triệu VNĐ/tháng",
        "xu_huong_phat_trien_nganh": ["Điện toán đám mây và kiến trúc Microservices", "Phát triển Low-code/No-code", "Trí tuệ nhân tạo (AI) và Học máy (ML) trong phát triển phần mềm", "Ứng dụng Web Tiến bộ (Progressive Web Apps - PWAs)", "DevSecOps (Tích hợp bảo mật vào quy trình DevOps)", "Blockchain trong ứng dụng phần mềm", "Internet of Things (IoT) software development", "Thực tế ảo (VR) và Thực tế tăng cường (AR)"],
        "thach_thuc_trong_nganh": ["Công nghệ thay đổi nhanh chóng, đòi hỏi học hỏi và cập nhật liên tục.", "Áp lực về thời gian và chất lượng sản phẩm trong các dự án.", "Yêu cầu cao về độ chính xác, tính bảo mật và hiệu năng của phần mềm.", "Cần khả năng làm việc độc lập và phối hợp tốt trong đội nhóm.", "Đối mặt với các vấn đề phức tạp và tìm kiếm giải pháp sáng tạo."]
    },
    {
        "chuyen_nganh": "Trí tuệ Nhân tạo (AI)",
        "mo_ta_chung": "Đào tạo kiến thức và kỹ năng để phát triển các hệ thống thông minh, ứng dụng học máy, xử lý ngôn ngữ tự nhiên và thị giác máy tính.",
        "mo_ta_chi_tiet_hon": "Chuyên ngành Trí tuệ Nhân tạo (AI) tập trung vào việc nghiên cứu và phát triển các hệ thống có khả năng mô phỏng trí thông minh của con người, như khả năng học hỏi, suy luận, nhận dạng mẫu, hiểu ngôn ngữ và đưa ra quyết định. Sinh viên sẽ được trang bị kiến thức nền tảng vững chắc về toán học, thống kê, các thuật toán học máy, học sâu, xử lý ngôn ngữ tự nhiên, thị giác máy tính và khoa học dữ liệu để có thể xây dựng và triển khai các ứng dụng AI giải quyết các bài toán thực tế trong nhiều lĩnh vực như y tế, tài chính, sản xuất, giao thông vận tải, và giải trí.",
        "mon_hoc_tieu_bieu": ["Nhập môn Trí tuệ nhân tạo", "Học máy (Machine Learning)", "Học sâu (Deep Learning)", "Xử lý ngôn ngữ tự nhiên (Natural Language Processing - NLP)", "Thị giác máy tính (Computer Vision)", "Khai phá dữ liệu (Data Mining)", "Khoa học dữ liệu (Data Science)", "Xử lý dữ liệu lớn (Big Data Analytics)", "Mạng nơ-ron nhân tạo (Neural Networks)", "Hệ chuyên gia và hệ trợ giúp quyết định", "Lập trình Python cho AI", "Toán học cho AI (Đại số tuyến tính, Xác suất thống kê, Giải tích)"],
        "ky_nang_can_thiet": {"ky_nang_ky_thuat": ["Kiến thức vững chắc về toán học (đại số tuyến tính, giải tích, xác suất thống kê)", "Thành thạo ngôn ngữ lập trình Python và các thư viện AI (TensorFlow, PyTorch, Keras, Scikit-learn, Pandas, NumPy)", "Hiểu biết sâu về các thuật toán học máy và học sâu", "Kỹ năng xử lý và phân tích dữ liệu lớn", "Kiến thức về xử lý ngôn ngữ tự nhiên và/hoặc thị giác máy tính", "Kỹ năng xây dựng và triển khai mô hình AI", "Kinh nghiệm làm việc với các nền tảng đám mây cho AI (AWS SageMaker, Google AI Platform, Azure ML)", "Kỹ năng trực quan hóa dữ liệu"], "ky_nang_mem": ["Tư duy phân tích và phản biện sắc bén", "Kỹ năng giải quyết vấn đề phức tạp", "Sự kiên nhẫn và bền bỉ trong nghiên cứu", "Khả năng học hỏi nhanh các công nghệ và thuật toán mới", "Kỹ năng giao tiếp để trình bày các giải pháp kỹ thuật phức tạp", "Sáng tạo và tư duy đổi mới", "Chú ý đến đạo đức trong AI (AI Ethics)"]},
        "cong_cu_va_cong_nghe_pho_bien": {"ngon_ngu_lap_trinh": ["Python (chủ đạo)", "R", "Java", "C++", "Lisp (trong nghiên cứu)"], "thu_vien_frameworks": ["TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "OpenCV", "NLTK", "spaCy", "Hugging Face Transformers"], "nen_tang_big_data": ["Apache Spark", "Hadoop", "Kafka"], "nen_tang_dam_may_ai": ["AWS SageMaker", "Google AI Platform & Vertex AI", "Microsoft Azure Machine Learning", "IBM Watson"], "cong_cu_khac": ["Jupyter Notebooks", "Google Colab", "Docker", "Kubeflow"]},
        "co_hoi_nghe_nghiep": ["Kỹ sư Trí tuệ Nhân tạo (AI Engineer)", "Kỹ sư Học máy (Machine Learning Engineer)", "Nhà khoa học dữ liệu (Data Scientist)", "Kỹ sư Xử lý ngôn ngữ tự nhiên (NLP Engineer)", "Kỹ sư Thị giác máy tính (Computer Vision Engineer)", "Nhà nghiên cứu AI (AI Researcher)", "Chuyên gia phân tích dữ liệu (Data Analyst)", "Kỹ sư Dữ liệu (Data Engineer - chuyên về pipeline cho AI)", "Chuyên gia Rô-bốt (Robotics Engineer - ứng dụng AI)", "Tư vấn giải pháp AI"],
        "muc_luong_khoi_diem": "15-30 triệu VNĐ/tháng",
        "xu_huong_phat_trien_nganh": ["AI Tạo sinh (Generative AI - ví dụ: LLMs, image generation)", "AI Giải thích được (Explainable AI - XAI)", "AI có trách nhiệm và đạo đức AI (Responsible AI & AI Ethics)", "Học tăng cường (Reinforcement Learning)", "TinyML (AI trên các thiết bị nhỏ, nhúng)", "Ứng dụng AI trong các ngành công nghiệp cụ thể (AI for Healthcare, Finance, etc.)", "Tự động hóa quy trình bằng Robot (RPA) kết hợp AI", "Edge AI (Xử lý AI tại biên)"],
        "thach_thuc_trong_nganh": ["Yêu cầu kiến thức chuyên sâu và liên tục cập nhật.", "Nguồn dữ liệu chất lượng cao và lớn là cần thiết cho việc huấn luyện mô hình.", "Các vấn đề về đạo đức, thiên kiến (bias) trong AI và quyền riêng tư.", "Khó khăn trong việc diễn giải một số mô hình AI phức tạp (black-box models).", "Cần nguồn lực tính toán lớn cho việc huấn luyện các mô hình học sâu.", "Sự thiếu hụt nhân lực chất lượng cao."]
    },
    {
        "chuyen_nganh": "Mạng Máy tính và An ninh mạng",
        "mo_ta_chung": "Đào tạo kiến thức và kỹ năng về thiết kế, xây dựng, vận hành, quản trị và bảo mật các hệ thống mạng máy tính, từ quy mô nhỏ đến lớn.",
        "mo_ta_chi_tiet_hon": "Chuyên ngành Mạng Máy tính và An ninh mạng cung cấp cho sinh viên nền tảng vững chắc về kiến trúc mạng, các giao thức truyền thông, kỹ thuật chuyển mạch và định tuyến, quản trị hệ thống mạng, cũng như các phương pháp, công cụ và chiến lược để đảm bảo an toàn thông tin cho hệ thống. Sinh viên sẽ học cách thiết kế, triển khai, giám sát, khắc phục sự cố và bảo vệ các tài sản thông tin, cơ sở hạ tầng mạng trước các mối đe dọa ngày càng tinh vi trong không gian mạng, bao gồm cả các giải pháp trên nền tảng điện toán đám mây.",
        "mon_hoc_tieu_bieu": ["Nhập môn Mạng máy tính", "Giao thức TCP/IP", "Thiết bị mạng (Router, Switch)", "Định tuyến và chuyển mạch (Routing & Switching)", "Mạng không dây (Wireless Networks)", "Quản trị hệ thống mạng (Network Administration)", "An ninh mạng cơ bản và nâng cao", "Mật mã học (Cryptography)", "An toàn hệ điều hành", "Phân tích và đánh giá an toàn thông tin", "Phòng chống tấn công mạng", "Điều tra số (Digital Forensics)", "Điện toán đám mây và bảo mật đám mây"],
        "ky_nang_can_thiet": {"ky_nang_ky_thuat": ["Hiểu biết sâu về các mô hình mạng (OSI, TCP/IP) và các giao thức mạng.", "Kỹ năng cấu hình và quản trị các thiết bị mạng (routers, switches, firewalls).", "Kiến thức về các hệ điều hành máy chủ (Linux, Windows Server).", "Kỹ năng triển khai và quản lý các dịch vụ mạng (DNS, DHCP, VPN).", "Kiến thức về các kỹ thuật tấn công và phòng thủ mạng.", "Kỹ năng sử dụng các công cụ giám sát và phân tích lưu lượng mạng (Wireshark, Nagios).", "Hiểu biết về các tiêu chuẩn và chính sách an ninh mạng.", "Kỹ năng về mật mã và an toàn thông tin.", "Kiến thức về bảo mật đám mây (Cloud Security).", "Kỹ năng scripting (Python, Bash) để tự động hóa tác vụ."], "ky_nang_mem": ["Tư duy phân tích và giải quyết vấn đề", "Chú ý đến chi tiết và cẩn trọng", "Kỹ năng làm việc dưới áp lực cao", "Khả năng ra quyết định nhanh chóng và chính xác", "Kỹ năng giao tiếp và làm việc nhóm", "Trung thực và có ý thức trách nhiệm cao", "Khả năng tự học và cập nhật các mối đe dọa mới."]},
        "cong_cu_va_cong_nghe_pho_bien": {"he_dieu_hanh": ["Linux (Ubuntu, CentOS, Kali Linux)", "Windows Server"], "thiet_bi_mang": ["Cisco", "Juniper", "Fortinet", "Palo Alto Networks", "MikroTik"], "cong_cu_bao_mat": ["Wireshark", "Nmap", "Metasploit", "Snort", "OSSEC", "Nessus", "SIEM systems (Splunk, ELK Stack)", "Firewalls (iptables, pfSense)"], "giao_thuc_cong_nghe_mang": ["TCP/IP", "DNS", "DHCP", "HTTP/S", "SSL/TLS", "VPN (IPSec, OpenVPN)", "VLANs", "SDN (Software-Defined Networking)", "NFV (Network Functions Virtualization)"], "nen_tang_dam_may": ["AWS (VPC, Security Groups, IAM)", "Azure (Virtual Network, NSG, Azure AD)", "GCP (VPC Network, Firewall Rules, IAM)"]},
        "co_hoi_nghe_nghiep": ["Kỹ sư mạng (Network Engineer)", "Chuyên viên quản trị mạng (Network Administrator)", "Chuyên viên an ninh mạng (Network Security Specialist/Analyst)", "Chuyên gia bảo mật thông tin (Information Security Officer/Consultant)", "Kỹ sư bảo mật hệ thống (Security Engineer)", "Chuyên viên phân tích mối đe dọa (Threat Analyst)", "Chuyên gia ứng phó sự cố an ninh (Incident Responder)", "Chuyên gia kiểm thử xâm nhập (Penetration Tester/Ethical Hacker)", "Kiến trúc sư an ninh mạng (Network Security Architect)", "Chuyên gia điện toán đám mây (Cloud Engineer - tập trung vào mạng và bảo mật)"],
        "muc_luong_khoi_diem": "12-22 triệu VNĐ/tháng",
        "xu_huong_phat_trien_nganh": ["Zero Trust Network Access (ZTNA)", "An ninh mạng cho IoT và OT (Operational Technology)", "Sử dụng AI và ML trong phát hiện và ứng phó mối đe dọa", "Tự động hóa an ninh mạng (Security Orchestration, Automation and Response - SOAR)", "Bảo mật đám mây (Cloud Security) và kiến trúc SASE (Secure Access Service Edge)", "Quyền riêng tư dữ liệu và tuân thủ quy định (Data Privacy & Compliance)", "Threat Intelligence Sharing"],
        "thach_thuc_trong_nganh": ["Các mối đe dọa mạng ngày càng tinh vi và liên tục phát triển.", "Cần cập nhật kiến thức và kỹ năng thường xuyên.", "Áp lực cao trong việc đảm bảo hệ thống luôn an toàn và hoạt động ổn định.", "Thiếu hụt nhân lực có tay nghề cao trong lĩnh vực an ninh mạng.", "Cân bằng giữa việc đảm bảo an ninh và sự tiện dụng cho người dùng.", "Đối mặt với các vấn đề pháp lý và đạo đức liên quan đến giám sát và quyền riêng tư."]
    },
    {
        "chuyen_nganh": "Hệ thống Thông tin",
        "mo_ta_chung": "Tập trung vào việc phân tích, thiết kế, phát triển, vận hành và quản lý các hệ thống thông tin để hỗ trợ hoạt động và ra quyết định trong các tổ chức, doanh nghiệp.",
        "mo_ta_chi_tiet_hon": "Chuyên ngành Hệ thống Thông tin đóng vai trò cầu nối giữa công nghệ thông tin và các hoạt động nghiệp vụ của tổ chức. Sinh viên được trang bị kiến thức về quản lý dự án, phân tích yêu cầu nghiệp vụ, thiết kế cơ sở dữ liệu, phát triển ứng dụng doanh nghiệp, quản trị hệ thống thông tin, và khai thác dữ liệu để hỗ trợ việc ra quyết định. Ngành này tập trung vào việc ứng dụng công nghệ để tối ưu hóa quy trình, nâng cao hiệu quả hoạt động, và tạo lợi thế cạnh tranh cho doanh nghiệp, bao gồm cả việc triển khai các giải pháp ERP, CRM, và thương mại điện tử.",
        "mon_hoc_tieu_bieu": ["Nhập môn Hệ thống thông tin quản lý (MIS)", "Phân tích và thiết kế hệ thống thông tin", "Cơ sở dữ liệu và Quản trị cơ sở dữ liệu", "Hệ quản trị cơ sở dữ liệu (Oracle, SQL Server, MySQL)", "Phát triển ứng dụng doanh nghiệp", "Hệ thống hoạch định nguồn lực doanh nghiệp (ERP)", "Quản lý quan hệ khách hàng (CRM)", "Thương mại điện tử (E-commerce)", "Khai phá dữ liệu và Kinh doanh thông minh (Data Mining & Business Intelligence - BI)", "Quản lý dự án công nghệ thông tin", "An toàn thông tin trong doanh nghiệp", "Kiểm toán hệ thống thông tin"],
        "ky_nang_can_thiet": {"ky_nang_ky_thuat": ["Kỹ năng phân tích yêu cầu nghiệp vụ và mô hình hóa quy trình.", "Kiến thức về thiết kế và quản trị cơ sở dữ liệu (SQL, NoSQL).", "Hiểu biết về các hệ thống ERP (SAP, Oracle NetSuite, Microsoft Dynamics 365) và CRM.", "Kỹ năng sử dụng các công cụ BI và trực quan hóa dữ liệu (Tableau, Power BI).", "Kiến thức về phát triển web và các ứng dụng doanh nghiệp.", "Hiểu biết về quản lý dự án và các phương pháp luận (Agile, Waterfall).", "Kiến thức cơ bản về an toàn thông tin và quản trị rủi ro.", "Kỹ năng làm việc với các công cụ phân tích dữ liệu (Excel nâng cao, Python/R cho phân tích cơ bản)."], "ky_nang_mem": ["Kỹ năng giao tiếp và làm việc với các bên liên quan (stakeholders).", "Tư duy hệ thống và khả năng nhìn nhận tổng thể.", "Kỹ năng giải quyết vấn đề và ra quyết định dựa trên dữ liệu.", "Kỹ năng quản lý dự án và tổ chức công việc.", "Khả năng làm việc nhóm và độc lập.", "Tư duy kinh doanh và hiểu biết về hoạt động của doanh nghiệp.", "Kỹ năng thuyết trình và đàm phán."]},
        "cong_cu_va_cong_nghe_pho_bien": {"he_quan_tri_csdl": ["Oracle Database", "Microsoft SQL Server", "MySQL", "PostgreSQL", "MongoDB"], "cong_cu_bi_truc_quan_hoa": ["Tableau", "Microsoft Power BI", "Qlik Sense", "Google Data Studio"], "he_thong_erp_crm": ["SAP S/4HANA", "Oracle NetSuite", "Microsoft Dynamics 365", "Salesforce", "Odoo"], "ngon_ngu_truy_van_lap_trinh": ["SQL", "Python (cho phân tích dữ liệu)", "Java (cho phát triển ứng dụng doanh nghiệp)", "C#"], "cong_cu_mo_hinh_hoa_quan_ly_du_an": ["Microsoft Visio", "Lucidchart", "Jira", "Microsoft Project", "Trello", "Asana"], "nen_tang_thuong_mai_dien_tu": ["Shopify", "Magento", "WooCommerce"]},
        "co_hoi_nghe_nghiep": ["Chuyên viên phân tích nghiệp vụ (Business Analyst - BA)", "Chuyên viên phân tích dữ liệu (Data Analyst)", "Chuyên viên quản trị cơ sở dữ liệu (Database Administrator - DBA)", "Chuyên gia tư vấn triển khai ERP/CRM", "Quản lý dự án Công nghệ Thông tin (IT Project Manager)", "Chuyên viên phát triển hệ thống thông tin", "Chuyên viên hỗ trợ hệ thống (System Support Specialist)", "Chuyên viên Kinh doanh thông minh (BI Analyst/Developer)", "Chuyên viên kiểm toán hệ thống thông tin (IT Auditor)", "Quản lý hệ thống thông tin (IT Manager)"],
        "muc_luong_khoi_diem": "10-20 triệu VNĐ/tháng",
        "xu_huong_phat_trien_nganh": ["Chuyển đổi số (Digital Transformation) trong doanh nghiệp.", "Phân tích dữ liệu lớn (Big Data Analytics) và Kinh doanh thông minh (BI) nâng cao.", "Điện toán đám mây (Cloud Computing) cho các giải pháp doanh nghiệp.", "Tự động hóa quy trình nghiệp vụ (Robotic Process Automation - RPA).", "Tăng cường bảo mật và quản trị dữ liệu.", "Ứng dụng AI và ML trong phân tích và dự báo kinh doanh.", "Phát triển các hệ thống thông tin tích hợp và linh hoạt."],
        "thach_thuc_trong_nganh": ["Cần sự kết hợp giữa kiến thức công nghệ và hiểu biết nghiệp vụ.", "Công nghệ thay đổi nhanh, đòi hỏi cập nhật liên tục các giải pháp mới.", "Khó khăn trong việc tích hợp các hệ thống cũ và mới.", "Quản lý sự thay đổi trong tổ chức khi triển khai hệ thống mới.", "Đảm bảo an toàn, bảo mật và tuân thủ quy định cho dữ liệu doanh nghiệp.", "Yêu cầu kỹ năng giao tiếp tốt để làm việc hiệu quả với nhiều phòng ban."]
    }
]

# Conversation history - sẽ được import và sử dụng bởi gui.py
messages = []

def initialize_openai_client():
    """Khởi tạo Azure OpenAI client và gán vào biến global `client`."""
    global client
    if subscription_key:
        try:
            client = AzureOpenAI(
                api_version=api_version,
                azure_endpoint=endpoint,
                api_key=subscription_key,
            )
            return True
        except Exception as e:
            print(f"Lỗi khi khởi tạo AzureOpenAI client: {e}")
            client = None  # Đảm bảo client là None nếu khởi tạo thất bại
            return False
    else:
        print("Lỗi: Azure OpenAI subscription key chưa được cung cấp.")
        client = None
        return False

def initialize_conversation_history():
    """Khởi tạo lịch sử hội thoại với thông tin chuyên ngành."""
    return [
        {"role": "system", "content": "Bạn là trợ lý tư vấn chọn chuyên ngành."},
        {"role": "assistant", "content": f"Dưới đây là thông tin các chuyên ngành:\n{json.dumps(data, ensure_ascii=False, indent=2)}"}
    ]

def chat_with_model(user_input_text, conversation_history):
    """
    Xử lý cuộc trò chuyện với mô hình Azure OpenAI.
    `conversation_history` là list `messages` được truyền từ `gui.py`.
    """
    global client  # Sử dụng client đã được khởi tạo

    if not client:
        return "Lỗi: Azure OpenAI client chưa được khởi tạo. Vui lòng kiểm tra API key và khởi động lại ứng dụng."

    # Nếu conversation_history rỗng, khởi tạo với dữ liệu mặc định
    if not conversation_history:
        conversation_history.extend(initialize_conversation_history())

    # Thêm tin nhắn người dùng vào lịch sử hội thoại
    conversation_history.append({"role": "user", "content": user_input_text})

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=conversation_history,
            max_tokens=4096,
            temperature=0.7,
            top_p=1.0,
        )
        assistant_reply = response.choices[0].message.content
        # Thêm câu trả lời của trợ lý vào lịch sử hội thoại
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    except Exception as e:
        print(f"Lỗi khi gọi Azure OpenAI: {e}")
        return "Xin lỗi, tôi đang gặp sự cố khi kết nối đến máy chủ AI. Vui lòng thử lại sau."