-- Tạo database


-- Bảng thông tin thú cưng
CREATE TABLE pets (
    pet_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    breed VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('Đực', 'Cái', 'Khác') NOT NULL,
    image_path VARCHAR(255),
    adoption_date DATE NOT NULL,
    health_status TEXT,
    preferences TEXT,
    special_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng lịch chăm sóc
CREATE TABLE care_schedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    event_type ENUM('Tiêm phòng', 'Tẩy giun', 'Khám định kỳ', 'Khác') NOT NULL,
    event_name VARCHAR(100) NOT NULL,
    scheduled_date DATETIME NOT NULL,
    reminder_date DATETIME NOT NULL,
    reminder_sent BOOLEAN DEFAULT FALSE,
    notes TEXT,
    google_calendar_event_id VARCHAR(255),
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng theo dõi sức khỏe
CREATE TABLE health_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    condition_name VARCHAR(100) NOT NULL,
    diagnosis_date DATE NOT NULL,
    symptoms TEXT,
    treatment TEXT,
    medications TEXT,
    vet_name VARCHAR(100),
    vet_contact VARCHAR(50),
    test_results_path VARCHAR(255),
    prescription_path VARCHAR(255),
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng chiều cao, cân nặng
CREATE TABLE physical_metrics (
    metric_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    weight_kg DECIMAL(5,2) NOT NULL,
    height_cm DECIMAL(5,2) NOT NULL,
    record_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng chi phí chăm sóc
CREATE TABLE expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    category ENUM('Thức ăn', 'Khám bệnh', 'Spa', 'Phụ kiện', 'Khác') NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    description TEXT,
    receipt_path VARCHAR(255),
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tạo view thống kê chi phí theo tháng
CREATE VIEW monthly_expenses AS
SELECT 
    YEAR(expense_date) AS year,
    MONTH(expense_date) AS month,
    category,
    SUM(amount) AS total_amount
FROM expenses
GROUP BY YEAR(expense_date), MONTH(expense_date), category
ORDER BY year, month, category;

-- Tạo view thống kê sức khỏe thú cưng
CREATE VIEW pet_health_summary AS
SELECT 
    p.pet_id,
    p.name,
    p.breed,
    p.age,
    p.gender,
    COUNT(DISTINCT h.record_id) AS health_records_count,
    COUNT(DISTINCT s.schedule_id) AS upcoming_schedules,
    MAX(pm.record_date) AS last_metric_date
FROM pets p
LEFT JOIN health_records h ON p.pet_id = h.pet_id
LEFT JOIN care_schedules s ON p.pet_id = s.pet_id AND s.scheduled_date > NOW()
LEFT JOIN physical_metrics pm ON p.pet_id = pm.pet_id
GROUP BY p.pet_id, p.name, p.breed, p.age, p.gender;

-- Tạo trigger cho thông báo lịch chăm sóc
DELIMITER //
CREATE TRIGGER set_reminder_date
BEFORE INSERT ON care_schedules
FOR EACH ROW
BEGIN
    IF NEW.reminder_date IS NULL THEN
        SET NEW.reminder_date = DATE_SUB(NEW.scheduled_date, INTERVAL 1 DAY);
    END IF;
END//
DELIMITER ;

-- Tạo stored procedure cho thống kê chi phí
DELIMITER //
CREATE PROCEDURE get_yearly_expenses(IN pet_id_param INT, IN year_param INT)
BEGIN
    SELECT 
        MONTH(expense_date) AS month,
        category,
        SUM(amount) AS total_amount
    FROM expenses
    WHERE 
        (pet_id = pet_id_param OR pet_id_param IS NULL) AND
        YEAR(expense_date) = year_param
    GROUP BY MONTH(expense_date), category
    ORDER BY month, category;
END//
DELIMITER ;